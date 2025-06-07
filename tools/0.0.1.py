#1 sudo timedatectl set-timezone Asia/Baghdad
#2 sudo systemctl restart systemd-timedated
# مكاتب التثبيت vps 👆🏻
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import schedule
from datetime import datetime
import time
import pytz
import re
from threading import Thread

API_TOKEN = "ᴛᴏ"
bot = telebot.TeleBot(API_TOKEN)

messages = {}
scheduled_messages = {}
admin_id = ɪᴅ# ايدي الادمن هنا 
channel_id = None  
moderators = set()  

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    if message.from_user.id != admin_id:
        markup.add(InlineKeyboardButton("أضف إعلان", callback_data="add_message"))  
        markup.row_width = 2
        markup.add(InlineKeyboardButton("قائمة الأعلانات", callback_data="show_scheduled"), 
                   InlineKeyboardButton("قناة الأعلانات", callback_data="show_channel"))
    else:
        markup.add(InlineKeyboardButton("أضف إعلان", callback_data="add_message"))  
        markup.row_width = 2
        markup.add(
            InlineKeyboardButton("قائمة الأعلانات", callback_data="show_scheduled"),  
            InlineKeyboardButton("قناة الأعلانات", callback_data="set_channel")
        )
        markup.row_width = 1
        markup.add(InlineKeyboardButton("إدارة المشرفين", callback_data="manage_admins"))  

    bot.send_message(message.chat.id, "أهلاً بكً في بوت أعلانات الأء .", reply_markup=markup)
                                        
@bot.callback_query_handler(func=lambda call: call.data == "show_channel")
def show_channel(call):
    if call.from_user.id in moderators:
        if channel_id:
            bot.send_message(call.message.chat.id, f"قناة الأعلانات : {channel_id}")
        else:
            bot.send_message(call.message.chat.id, "لم يتم تحديد قناة الأعلانات بعد .")
    else:
        bot.answer_callback_query(call.id, "لا يمكنك عرض قناة الأعلانات .", show_alert=True)
                    
@bot.callback_query_handler(func=lambda call: call.data == "set_channel")
def set_channel(call):
    if call.from_user.id == admin_id or call.from_user.id in moderators:
        bot.send_message(call.message.chat.id, "أرسل يوزر القناة مثل @channel أو -1001234567890) .")
        bot.register_next_step_handler(call.message, save_channel)
    else:
        bot.answer_callback_query(call.id, "لا يمكنك اضافة قنوات .", show_alert=True)
        
def save_channel(message):
    global channel_id
    channel_text = message.text
    if re.match(r"^@[\w\d_]+$", channel_text) or re.match(r"^(-100\d{10})$", channel_text):
        channel_id = channel_text
        bot.send_message(message.chat.id, f"تم حفظ قناة الأعلانات: {channel_id}")
    else:
        bot.send_message(message.chat.id, "الرجاء إدخال معرف قناة صحيح يتضمن @ أو رقم المعرف.")
        return
                   
@bot.callback_query_handler(func=lambda call: call.data == "manage_admins")
def manage_admins(call):
    if call.from_user.id == admin_id:
        markup = InlineKeyboardMarkup(row_width=1)  
        markup.add(InlineKeyboardButton("رفع مشرف", callback_data="add_moderator"))
        markup.row_width = 2 
        markup.add(
            InlineKeyboardButton("تنزيل مشرف", callback_data="remove_moderator"),
            InlineKeyboardButton("عرض المشرفين", callback_data="show_moderators")
        )

        markup.row_width = 1 
        markup.add(InlineKeyboardButton("⬅️ رجوع", callback_data="back_to_main"))

        bot.edit_message_text("إدارة المشرفين:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call):
    if call.from_user.id == admin_id or call.from_user.id in moderators:
        markup = InlineKeyboardMarkup(row_width=1)  
        markup.add(InlineKeyboardButton("أضف إعلان", callback_data="add_message"))
        markup.row_width = 2 
        markup.add(
            InlineKeyboardButton("قائمة الأعلانات", callback_data="show_scheduled"),
            InlineKeyboardButton("إدارة المشرفين", callback_data="manage_admins")
        )

        markup.row_width = 1  
        markup.add(InlineKeyboardButton("قناة الأعلانات", callback_data="set_channel"))

        bot.edit_message_text("أهلاً بكً في بوت أعلانات الأء .", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
        
@bot.callback_query_handler(func=lambda call: call.data == "add_moderator")
def add_moderator(call):
    if call.from_user.id == admin_id:
        bot.send_message(call.message.chat.id, "أرسل ايدي الشخص الذي تريد رفعه كمشرف .")
        bot.register_next_step_handler(call.message, save_moderator)

def save_moderator(message):
    try:
        user_id = int(message.text)
        if user_id in moderators or user_id == admin_id:
            bot.send_message(message.chat.id, "هذا المستخدم بالفعل مشرف .")
        else:
            moderators.add(user_id)
            bot.send_message(message.chat.id, f"تم رفع المستخدم {user_id} كمشرف .")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إدخال معرف صحيح .")

@bot.callback_query_handler(func=lambda call: call.data == "remove_moderator")
def remove_moderator(call):
    if call.from_user.id == admin_id:
        bot.send_message(call.message.chat.id, "أرسل معرف المستخدم الذي تريد تنزيله من المشرفين .")
        bot.register_next_step_handler(call.message, delete_moderator)

def delete_moderator(message):
    try:
        user_id = int(message.text)      
        if user_id == admin_id:
            bot.send_message(message.chat.id, "لا يمكنك تنزيل نفسك من قائمة المشرفين .")
            return
        
        if user_id in moderators:
            moderators.remove(user_id)
            bot.send_message(message.chat.id, f"تم تنزيل المستخدم {user_id} من المشرفين .")           
            if user_id == message.from_user.id:
                bot.send_message(message.chat.id, "لقد تم تنزيلك من قائمة المشرفين. لم تعد لديك صلاحية التحكم في الأزرار.")
                return  

        else:
            bot.send_message(message.chat.id, "هذا المستخدم ليس مشرف .")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إدخال معرف صحيح .")
        
@bot.callback_query_handler(func=lambda call: call.data == "show_moderators")
def show_moderators(call):
    if call.from_user.id == admin_id:
        if moderators:
            moderator_list = "\n".join(str(mod) for mod in moderators)
            bot.send_message(call.message.chat.id, f"قائمة المشرفين:\n{moderator_list}")
        else:
            bot.send_message(call.message.chat.id, "لا يوجد مشرفين حاليًا .")

@bot.callback_query_handler(func=lambda call: call.data == "add_message")
def ask_for_message(call):
    if call.from_user.id == admin_id or call.from_user.id in moderators:
        if not channel_id:
            bot.send_message(call.message.chat.id, "لم تقم بتحديد قناة لنشر الأعلانات بعد .")
            return  
        
        bot.send_message(call.message.chat.id, "دزلي الأعلان هسه .")
        bot.register_next_step_handler(call.message, save_message)
    else:
        bot.answer_callback_query(call.id, "أنت غير مسموح لك بإضافة إعلانات .", show_alert=True)
        return
        
def save_message(message):
    messages['content'] = message.text
    bot.send_message(message.chat.id, "تم حفظ الأعلان .\nدزلي هسه وقت نشر الأعلان ووقت حذف الأعلان \n\nمثال:\n`1:00ص 2:00م`", parse_mode="Markdown")   
    bot.register_next_step_handler(message, save_times)

def save_times(message):
    try:
        times = message.text.split()
        publish_time = times[0]
        delete_time = times[1]
        if not is_valid_time(publish_time) or not is_valid_time(delete_time):
            raise ValueError("Invalid time format")

        message_id = len(scheduled_messages) + 1
        scheduled_messages[message_id] = {
            "content": messages['content'],
            "publish_time": publish_time,
            "delete_time": delete_time,
        }

        bot.send_message(
            message.chat.id,
            f"تم حفظ الأعلان بنجاح:\nوقت النشر: {publish_time}\nوقت الحذف: {delete_time}",
            reply_markup=get_scheduled_button()
        )
        
        schedule_message(message_id, publish_time, delete_time)
    except Exception:
        bot.send_message(message.chat.id, "هناك خطأ في تنسيق الوقت. الرجاء إعادة المحاولة بالتنسيق الصحيح.")

def get_scheduled_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("قائمة الأعلانات", callback_data="show_scheduled"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "show_scheduled")
def show_scheduled(call):
    if call.from_user.id not in moderators and call.from_user.id != admin_id:
        bot.answer_callback_query(call.id, "أنت غير مسموح لك بعرض الإعلانات .", show_alert=True)
        return

    if not scheduled_messages:
        bot.send_message(call.message.chat.id, "لا توجد إعلانات حاليًا .")
        return

    for message_id, details in scheduled_messages.items():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🗑️", callback_data=f"delete_{message_id}"))
        bot.send_message(
            call.message.chat.id,
            f"الأعلان رقم #{message_id}:\n\n{details['content']}\n\n"
            f"وقت النشر: {details['publish_time']}\n"
            f"وقت الحذف: {details['delete_time']}",
            reply_markup=markup,
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_scheduled(call):
    message_id = int(call.data.split("_")[1])
    if message_id in scheduled_messages:
        message_obj = scheduled_messages[message_id].get('message_obj')
        
        if message_obj:
            bot.delete_message(channel_id, message_obj.message_id)
            bot.send_message(call.message.chat.id, f"تم حذف الإعلان رقم {message_id} من القناة بنجاح .")
            del scheduled_messages[message_id]
        else:
            del scheduled_messages[message_id]
            bot.send_message(call.message.chat.id, f"تم حذف الإعلان رقم {message_id} من القائمة لن يتم نشره .")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        bot.send_message(call.message.chat.id, "هذا الإعلان غير موجود أو تم حذفه بالفعل .")
                
def schedule_message(message_id, publish_time, delete_time):
    publish_time_24 = format_time_24(publish_time)
    delete_time_24 = format_time_24(delete_time)
    
    if not publish_time_24 or not delete_time_24:
        print("Error: Invalid time format for scheduling.")
        return

    def publish():
        if message_id in scheduled_messages:
            scheduled_messages[message_id]['message_obj'] = bot.send_message(
                channel_id, f"{scheduled_messages[message_id]['content']}"
            )
            print(f"Message {message_id} published.")

    def delete():
        if message_id in scheduled_messages:
            message_obj = scheduled_messages[message_id].get('message_obj')
            if message_obj:
                bot.delete_message(channel_id, message_obj.message_id)
            del scheduled_messages[message_id]
            print(f"Message {message_id} deleted.")

    schedule.every().day.at(publish_time_24).do(publish)
    schedule.every().day.at(delete_time_24).do(delete)
    
def format_time_24(time_str):
    try:
        tz = pytz.timezone("Asia/Baghdad")
        time_str = time_str.replace('ص', 'AM').replace('م', 'PM')
        naive_time = datetime.strptime(time_str, "%I:%M%p")
        localized_time = tz.localize(naive_time)
        return localized_time.strftime("%H:%M")
    except Exception as e:
        print(f"Error in format_time_24: {e}")
        return None
            
def is_valid_time(time_str):
    try:
        tz = pytz.timezone("Asia/Baghdad")  
        time_str = time_str.replace('ص', 'AM').replace('م', 'PM') 
        naive_time = datetime.strptime(time_str, "%I:%M%p")
        localized_time = tz.localize(naive_time)
        return True
    except ValueError:
        return False

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=run_scheduler, daemon=True).start()
    bot.polling()