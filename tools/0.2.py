import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7429060374:AAGo_sBZFtjcsCh_9hMhyb0jsmmEVRWhcVI'
id = 7538765829
bot = telebot.TeleBot(TOKEN)

sessions = {}
banned_users = set()
admins = {id}

users_data = {}

forced_channel = None
forced_subscription = False
communication_enabled = True

def save_users_data():
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=4)

def load_users_data():
    global users_data
    try:
        with open('users.json', 'r') as f:
            users_data = json.load(f)
    except FileNotFoundError:
        users_data = {}

load_users_data()

@bot.message_handler(commands=['start'])
def start_cmd(m):
    u_id = m.from_user.id
    if str(u_id) not in users_data:
        users_data[str(u_id)] = {
            'first_name': m.from_user.first_name,
            'username': m.from_user.username,
            'id': u_id
        }
        save_users_data()

    if forced_subscription and forced_channel:
        member = bot.get_chat_member(forced_channel, u_id)
        if member.status not in ['member', 'administrator', 'creator']:
            bot.send_message(u_id, f"الرجاء الاشتراك في القناة أولاً: {forced_channel}")
            return

    bot.send_message(u_id, "✨ Welcome ✨

Welcome to our community, where communication becomes easier and more fun. I am your loyal assistant, always ready to help.

What can I do for you:
- 💬 Communication: I will support the conversation and answer your questions.
- 📚 Information: I will provide useful information and tips.
- 🔧 Help: I will help with various tasks and find solutions.

Feel free to contact me with any questions or suggestions. Let s start our interaction !

- Leave your message and it will be answered.")

@bot.message_handler(commands=['admin'])
def admin_cmd(m):
    if m.chat.id not in admins:
        bot.send_message(m.chat.id, "ليس لديك صلاحيات الوصول إلى لوحة التحكم.")
        return

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🚫 حظر", callback_data='ban'),
        InlineKeyboardButton("✅ فك حظر", callback_data='unban'),
        InlineKeyboardButton("➕ إضافة أدمن", callback_data='add_admin'),
        InlineKeyboardButton("➖ حذف أدمن", callback_data='remove_admin'),
        InlineKeyboardButton("📢 إذاعة", callback_data='broadcast'),
        InlineKeyboardButton("📊 إحصائيات", callback_data='stats'),
        InlineKeyboardButton("💾 تخزين البيانات", callback_data='export_json'),
        InlineKeyboardButton("🔒 تفعيل الاشتراك الإجباري", callback_data='enable_forced_sub'),
        InlineKeyboardButton("🔓 إيقاف الاشتراك الإجباري", callback_data='disable_forced_sub'),
        InlineKeyboardButton("➕ إضافة قناة اشتراك", callback_data='add_channel'),
        InlineKeyboardButton("📬 تفعيل التواصل", callback_data='enable_communication'),
        InlineKeyboardButton("📴 إيقاف التواصل", callback_data='disable_communication')
    )
    bot.send_message(m.chat.id, "اهلا بك عزيزي المالك في لوحة التحكم الخاصه بك ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.message.chat.id not in admins:
        return

    if call.data == 'ban':
        msg = bot.send_message(call.message.chat.id, "أرسل معرف أو آيدي المستخدم لحظره:")
        bot.register_next_step_handler(msg, ban_user)
    elif call.data == 'unban':
        msg = bot.send_message(call.message.chat.id, "أرسل معرف أو آيدي المستخدم لفك حظره:")
        bot.register_next_step_handler(msg, unban_user)
    elif call.data == 'add_admin':
        msg = bot.send_message(call.message.chat.id, "أرسل معرف أو آيدي المستخدم لإضافته كأدمن:")
        bot.register_next_step_handler(msg, add_admin)
    elif call.data == 'remove_admin':
        msg = bot.send_message(call.message.chat.id, "أرسل معرف أو آيدي المستخدم لحذفه من الأدمن:")
        bot.register_next_step_handler(msg, remove_admin)
    elif call.data == 'broadcast':
        msg = bot.send_message(call.message.chat.id, "أرسل الرسالة التي تريد إذاعتها:")
        bot.register_next_step_handler(msg, broadcast_message)
    elif call.data == 'stats':
        show_stats()
    elif call.data == 'export_json':
        export_json()
    elif call.data == 'enable_forced_sub':
        global forced_subscription
        forced_subscription = True
        bot.send_message(call.message.chat.id, "تم تفعيل الاشتراك الإجباري.")
    elif call.data == 'disable_forced_sub':
        forced_subscription = False
        bot.send_message(call.message.chat.id, "تم إيقاف الاشتراك الإجباري.")
    elif call.data == 'add_channel':
        msg = bot.send_message(call.message.chat.id, "أرسل معرف القناة لإضافتها:")
        bot.register_next_step_handler(msg, set_forced_channel)
    elif call.data == 'enable_communication':
        global communication_enabled
        communication_enabled = True
        bot.send_message(call.message.chat.id, "تم تفعيل التواصل.")
    elif call.data == 'disable_communication':
        communication_enabled = False
        bot.send_message(call.message.chat.id, "تم إيقاف التواصل.")

def ban_user(m):
    u = m.text.strip()
    if u.isdigit():
        banned_users.add(int(u))
    else:
        banned_users.add(u)
    bot.send_message(m.chat.id, "تم حظر المستخدم.")

def unban_user(m):
    u = m.text.strip()
    if u.isdigit():
        banned_users.discard(int(u))
    else:
        banned_users.discard(u)
    bot.send_message(m.chat.id, "تم فك حظر المستخدم.")

def add_admin(m):
    u = m.text.strip()
    try:
        if u.isdigit():
            u = int(u)
            admins.add(u)
            bot.send_message(m.chat.id, "تمت إضافة الأدمن بنجاح.")
        else:
            user = bot.get_chat(u)
            admins.add(user.id)
            bot.send_message(m.chat.id, "تمت إضافة الأدمن بنجاح.")
    except Exception as e:
        bot.send_message(m.chat.id, "تعذر إضافة الأدمن. تحقق من صحة المعرف أو الآيدي.")

def remove_admin(m):
    u = m.text.strip()
    if u.isdigit():
        admins.discard(int(u))
    else:
        try:
            user = bot.get_chat(u)
            admins.discard(user.id)
        except Exception as e:
            bot.send_message(m.chat.id, "تعذر إزالة الأدمن. تحقق من صحة المعرف أو الآيدي.")
    bot.send_message(m.chat.id, "تمت إزالة الأدمن.")

def broadcast_message(m):
    msg = m.text.strip()
    for u_id in users_data:
        bot.send_message(int(u_id), msg)
    bot.send_message(m.chat.id, "تم إرسال الرسالة إلى جميع المستخدمين.")

def show_stats():
    num_users = len(users_data)
    last_ten = list(users_data.values())[-10:]
    stats_message = f"عدد المستخدمين: {num_users}\nآخر 10 أعضاء:\n"
    for u in last_ten:
        stats_message += f"name : {u['first_name']}\nuser : @{u['username']}\nID: {u['id']}\n______________\n"
    bot.send_message(id, stats_message)

def export_json():
    with open('users.json', 'rb') as f:
        bot.send_document(id, f)

def set_forced_channel(m):
    global forced_channel
    channel_id = m.text.strip()
    try:
        bot.get_chat_member(channel_id, id)
        forced_channel = channel_id
        bot.send_message(m.chat.id, f"تم تعيين قناة الاشتراك: {forced_channel}")
    except Exception as e:
        bot.send_message(m.chat.id, "تعذر إضافة القناة. تأكد من أن البوت مشرف في القناة.")

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    u_id = m.chat.id
    
    if u_id in banned_users:
        return

    if not communication_enabled:
        if u_id != id:
            bot.send_message(u_id, f"تم إيقاف استلام الرسائل من قبل المالك. @{bot.get_chat(id).username}")
        return
    
    if u_id != id:
        sessions[u_id] = m.message_id
        bot.send_message(id, f"new message from : @{m.from_user.username}:\nmessage : {m.text}")
        bot.send_message(u_id, "We will reply soon, just wait? 🌸")
    else:
        if m.reply_to_message:
            user_id = None
            for user_id, msg_id in sessions.items():
                if m.reply_to_message.message_id == msg_id:
                    break
            if user_id:
                bot.send_message(user_id, f"رد من المالك:\n{m.text}")
            else:
                bot.send_message(id, "تعذر العثور على المستخدم الأصلي.")
        else:
            bot.send_message(id, "يرجى الرد على رسالة لتوجيهها للمستخدم.")

bot.polling()