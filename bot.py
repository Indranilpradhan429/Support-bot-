import telebot
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = "users.txt"
STATS_FILE = "stats.txt"

def get_users():
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r") as f:
        return set([x for x in f.read().splitlines() if x.strip()])

def add_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")
        with open(STATS_FILE, "a") as f:
            f.write(f"{user_id},{datetime.now().strftime('%Y-%m-%d')}\n")

@bot.message_handler(commands=['start'])
def start(m):
    add_user(m.chat.id)
    bot.send_message(m.chat.id, "Hi! Send your message here. Admin will reply you soon.")

@bot.message_handler(commands=['broadcast','botcast','users','stats','stat'])
def admin_cmd(m):
    if m.chat.id != ADMIN_ID:
        return
    text = m.text.lower()
    if text.startswith("/users") or text.startswith("/stats") or text.startswith("/stat"):
        users = get_users()
        total = len(users)
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_count = 0
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r") as f:
                for line in f:
                    if today_str in line:
                        today_count+=1
        msg = f"📊 Bot Statistics\n\n👥 Total Users: {total}\n📅 Joined Today: {today_count}\n🤖 Bot Status: Online\n🕒 Time: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
        bot.send_message(ADMIN_ID, msg)
        return
    else:
        msg_text = m.text.replace("/broadcast","").replace("/botcast","").strip()
        users = get_users()
        count = 0
        if not msg_text and m.reply_to_message:
            for uid in users:
                try:
                    bot.copy_message(int(uid), m.chat.id, m.reply_to_message.message_id)
                    count+=1
                except: pass
            bot.send_message(ADMIN_ID, f"Broadcast sent to {count} users.")
            return
        if not msg_text:
            bot.send_message(ADMIN_ID, "Usage: /broadcast Your message\nOr reply to a message with /broadcast")
            return
        for uid in users:
            try:
                bot.send_message(int(uid), msg_text)
                count+=1
            except: pass
        bot.send_message(ADMIN_ID, f"Broadcast sent to {count} users.")

@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','document','sticker'])
def handle(m):
    if m.chat.id == ADMIN_ID:
        if m.reply_to_message and m.reply_to_message.forward_from:
            try:
                bot.copy_message(m.reply_to_message.forward_from.id, m.chat.id, m.message_id)
            except:
                bot.send_message(ADMIN_ID, "Please reply on forwarded message.")
    else:
        add_user(m.chat.id)
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.send_message(m.chat.id, "Your message has been sent to admin. You will get a reply soon.")

bot.infinity_polling()
