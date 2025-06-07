import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import quote
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "token"

BASE_URL = "https://www.hindawi.org"
SEARCH_URL_TEMPLATE = f"{BASE_URL}/search/keyword/{{query}}/"

BOOKS_PER_PAGE = 5  # عدد الكتب التي تظهر  ب كل صفحة نتائج بحث

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

user_states = {}
user_data = {}

STATE_AWAITING_BOOK_NAME = 0
STATE_AWAITING_BOOK_CHOICE = 1
STATE_AWAITING_FORMAT_CHOICE = 2

def delete_bot_previous_message(chat_id):
    if chat_id in user_data and 'last_bot_message_id' in user_data[chat_id]:
        message_id_to_delete = user_data[chat_id]['last_bot_message_id']
        try:
            bot.delete_message(chat_id, message_id_to_delete)
        except telebot.apihelper.ApiTelegramException as e:
            logger.warning(f"فشل حذف رسالة البوت السابقة (قد تكون قديمة أو محذوفة): {e}")
        finally:
            if 'last_bot_message_id' in user_data[chat_id]:
                del user_data[chat_id]['last_bot_message_id']

def send_and_store_message(chat_id, text, reply_markup=None):
    sent_message = bot.send_message(chat_id, text, reply_markup=reply_markup)
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]['last_bot_message_id'] = sent_message.message_id

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! 👋 أنا هنا لمساعدتك في العثور على الكتب من مؤسسة هنداوي. أرسل لي اسم الكتاب الذي تبحث عنه 📚، أو استخدم /search.")
    user_states[message.chat.id] = STATE_AWAITING_BOOK_NAME

@bot.message_handler(commands=['search'])
def prompt_search(message):
    bot.reply_to(message, "رجاءً، أرسل اسم الكتاب الذي تود البحث عنه. 🔍")
    user_states[message.chat.id] = STATE_AWAITING_BOOK_NAME

@bot.message_handler(commands=['cancel'])
def cancel_operation(message):
    delete_bot_previous_message(message.chat.id)
    if message.chat.id in user_states:
        del user_states[message.chat.id]
    if message.chat.id in user_data:
        del user_data[message.chat.id]
    bot.reply_to(message, "تم الإلغاء بنجاح. ✅")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_AWAITING_BOOK_NAME and message.text)
def handle_book_search(message):
    chat_id = message.chat.id
    book_name = message.text.strip()

    if not book_name:
        bot.reply_to(message, "الرجاء إرسال اسم كتاب صالح للبحث. 📝")
        return
    
    encoded_book_name = quote(book_name)
    search_url = SEARCH_URL_TEMPLATE.format(query=encoded_book_name)

    bot.send_message(chat_id, f"جاري البحث عن '{book_name}'... الرجاء الانتظار قليلاً. ⏳")

    try:
        response = requests.get(search_url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        found_books = []
        for link_tag in soup.find_all('a', href=True):
            href = link_tag.get('href')
            if href and re.match(r'/books/\d{6,}/$', href):
                full_url = requests.compat.urljoin(BASE_URL, href)
                book_title_from_search = link_tag.get_text(strip=True)

                if not book_title_from_search or "كتاب بعنوان" in book_title_from_search:
                    img_tag = link_tag.find('img', alt=True)
                    if img_tag and img_tag.get('alt'):
                        book_title_from_search = img_tag.get('alt').replace(' كتاب بعنوان ', '').strip()
                
                if not book_title_from_search:
                    book_title_from_search = href.strip('/').split('/')[-1]

                if (full_url, book_title_from_search) not in [(item[0], item[1]) for item in found_books]:
                    found_books.append((full_url, book_title_from_search))
            
        user_data[chat_id] = {'found_books': found_books, 'current_page': 0}

        if not found_books:
            bot.send_message(chat_id, "عذراً، لم يتم العثور على أي كتاب بهذا الاسم. 😔 هل تود البحث عن اسم آخر؟")
            user_states[chat_id] = STATE_AWAITING_BOOK_NAME
            return
        
        send_book_results_page(chat_id, 0) # إرسال الصفحة الأولى من النتائج

    except requests.exceptions.RequestException as e:
        logger.error(f"حدث خطأ أثناء الاتصال بالبحث: {e}")
        bot.send_message(chat_id, "حدث خطأ ما أثناء البحث. 🚫 الرجاء المحاولة لاحقاً، أو أرسل `/cancel`.")
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in user_data: del user_data[chat_id]

def send_book_results_page(chat_id, page_num):
    found_books = user_data[chat_id]['found_books']
    user_data[chat_id]['current_page'] = page_num

    start_index = page_num * BOOKS_PER_PAGE
    end_index = start_index + BOOKS_PER_PAGE
    books_on_page = found_books[start_index:end_index]

    message_text = "تم العثور على الكتب التالية: 📚\n"
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for i, (url, title) in enumerate(books_on_page):
        # نستخدم مؤشر الكتاب الحقيقي في القائمة الكاملة، وليس مؤشر الصفحة
        real_index = start_index + i 
        keyboard.add(types.InlineKeyboardButton(text=title, callback_data=f"book_choice_{real_index}"))
    
    pagination_buttons = []
    if page_num > 0:
        pagination_buttons.append(types.InlineKeyboardButton(text="⬅️ الصفحة السابقة", callback_data=f"prev_page_{page_num - 1}"))
    
    if end_index < len(found_books):
        pagination_buttons.append(types.InlineKeyboardButton(text="الصفحة التالية ➡️", callback_data=f"next_page_{page_num + 1}"))
    
    if pagination_buttons:
        keyboard.add(*pagination_buttons)

    keyboard.add(types.InlineKeyboardButton(text="إلغاء البحث ❌", callback_data="cancel_search"))

    delete_bot_previous_message(chat_id)
    send_and_store_message(chat_id, message_text, reply_markup=keyboard)
    user_states[chat_id] = STATE_AWAITING_BOOK_CHOICE

@bot.callback_query_handler(func=lambda call: user_states.get(call.message.chat.id) == STATE_AWAITING_BOOK_CHOICE and call.data.startswith(('book_choice_', 'next_page_', 'prev_page_', 'cancel_search')))
def handle_book_choice_inline(call):
    chat_id = call.message.chat.id
    data = call.data
    bot.answer_callback_query(call.id) # إزالة حالة التحميل من الزر

    if data.startswith('book_choice_'):
        choice_index = int(data.split('_')[2])
        found_books = user_data.get(chat_id, {}).get('found_books')

        if not found_books or not (0 <= choice_index < len(found_books)):
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="عذراً، هذا الخيار غير صالح. 🧐")
            if chat_id in user_states: del user_states[chat_id]
            if chat_id in user_data: del user_data[chat_id]
            return
        
        selected_book_url, _ = found_books[choice_index]
        user_data[chat_id]['selected_book_url'] = selected_book_url

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="جاري جلب تفاصيل الكتاب... ⏳ الرجاء الانتظار.")
        
        try:
            book_response = requests.get(selected_book_url, timeout=30)
            book_response.raise_for_status()

            soup = BeautifulSoup(book_response.text, 'html.parser')
            
            book_title_tag = soup.find('title')
            actual_book_title = "كتاب_غير_معنون"
            if book_title_tag and book_title_tag.string:
                actual_book_title = book_title_tag.string.replace(' | مؤسسة هنداوي', '').strip()
                actual_book_title = re.sub(r'[\\/:*?"<>|]', '', actual_book_title)
            
            user_data[chat_id]['actual_book_title'] = actual_book_title
            
            available_formats = {}
            for dl_tag in soup.find_all('a', href=True):
                dl_href = dl_tag.get('href')
                if dl_href and dl_href.endswith(('.pdf', '.epub', '.kfx')):
                    format_name = dl_href.split('.')[-1].upper()
                    full_dl_url = requests.compat.urljoin(BASE_URL, dl_href)
                    available_formats[format_name] = full_dl_url
            
            user_data[chat_id]['available_formats'] = available_formats

            if not available_formats:
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="عذراً، لا توجد صيغ متوفرة لهذا الكتاب حالياً. 😔")
                if chat_id in user_states: del user_states[chat_id]
                if chat_id in user_data: del user_data[chat_id]
                return

            message_text = "الصيغ المتوفرة: 📄\n"
            sorted_formats_keys = sorted(available_formats.keys())
            keyboard_formats = types.InlineKeyboardMarkup(row_width=1)
            for format_name in sorted_formats_keys:
                keyboard_formats.add(types.InlineKeyboardButton(text=format_name, callback_data=f"format_choice_{format_name}"))
            keyboard_formats.add(types.InlineKeyboardButton(text="إلغاء التنزيل ❌", callback_data="cancel_download"))

            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard_formats)
            user_states[chat_id] = STATE_AWAITING_FORMAT_CHOICE

        except requests.exceptions.RequestException as e:
            logger.error(f"حدث خطأ أثناء جلب تفاصيل الكتاب: {e}")
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="حدث خطأ ما أثناء جلب تفاصيل الكتاب. 🚫 الرجاء المحاولة لاحقاً، أو أرسل `/cancel`.")
            if chat_id in user_states: del user_states[chat_id]
            if chat_id in user_data: del user_data[chat_id]

    elif data.startswith('next_page_'):
        next_page = int(data.split('_')[2])
        send_book_results_page(chat_id, next_page)
    elif data.startswith('prev_page_'):
        prev_page = int(data.split('_')[2])
        send_book_results_page(chat_id, prev_page)
    elif data == 'cancel_search':
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="تم الإلغاء بنجاح. ✅")
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in user_data: del user_data[chat_id]

@bot.callback_query_handler(func=lambda call: user_states.get(call.message.chat.id) == STATE_AWAITING_FORMAT_CHOICE and call.data.startswith(('format_choice_', 'cancel_download')))
def handle_format_choice_and_download_inline(call):
    chat_id = call.message.chat.id
    data = call.data
    bot.answer_callback_query(call.id) # إزالة حالة التحميل من الزر

    if data.startswith('format_choice_'):
        chosen_format_name = data.split('_')[2]
        available_formats = user_data.get(chat_id, {}).get('available_formats')
        
        if not available_formats or chosen_format_name not in available_formats:
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="عذراً، هذا الخيار غير صالح. 🧐")
            if chat_id in user_states: del user_states[chat_id]
            if chat_id in user_data: del user_data[chat_id]
            return
        
        chosen_format_url = available_formats[chosen_format_name]

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="جاري إرسال الملف... 📤 قد يستغرق ذلك بعض الوقت.")
        
        try:
            bot_info = bot.get_me()
            bot_username = f"@{bot_info.username}" if bot_info.username else "البوت"
            caption_text = f"{bot_username} ⬇️"

            bot.send_document(chat_id, chosen_format_url, caption=caption_text)

            bot.send_message(chat_id, "تم تنزيل الكتاب بنجاح! 🎉")

            if chat_id in user_states: del user_states[chat_id]
            if chat_id in user_data: del user_data[chat_id]

        except telebot.apihelper.ApiTelegramException as send_e:
            logger.error(f"فشل إرسال الملف عبر تليجرام: {send_e}", exc_info=True)
            bot.send_message(chat_id, "حدث خطأ أثناء إرسال الملف. 🚫 الرجاء المحاولة مرة أخرى.")
            if chat_id in user_states: del user_states[chat_id]
            if chat_id in user_data: del user_data[chat_id]
        except Exception as e:
            logger.error(f"حدث خطأ غير متوقع: {e}", exc_info=True)
            bot.send_message(chat_id, "حدث خطأ غير متوقع. ❌ الرجاء المحاولة مرة أخرى، أو أرسل `/cancel`.")
            if chat_id in user_states: del user_states[chat_id]
            if chat_id in user_data: del user_data[chat_id]
    
    elif data == 'cancel_download':
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="تم الإلغاء بنجاح. ✅")
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in user_data: del user_data[chat_id]

@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    delete_bot_previous_message(message.chat.id)
    if user_states.get(message.chat.id) not in [STATE_AWAITING_BOOK_NAME, STATE_AWAITING_BOOK_CHOICE, STATE_AWAITING_FORMAT_CHOICE]:
        bot.send_message(message.chat.id, "رسالة غير مفهومة. 😕 للبحث عن كتاب، أرسل اسمه مباشرة أو استخدم الأمر `/search`.")
        user_states[message.chat.id] = STATE_AWAITING_BOOK_NAME
    else:
        bot.reply_to(message, "رسالة غير مفهومة. 😕 للبحث عن كتاب، أرسل اسمه مباشرة أو استخدم الأمر `/search`.")

def main():
    logger.info("تم بدء استطلاع البوت...")
    bot.polling(none_stop=True, interval=0, timeout=20)

if __name__ == "__main__":
    main()
