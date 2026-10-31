import telebot
import os

BOT_TOKEN = os.getenv("9112482269:AAEUnjb0VsjFtjpVjlA0HZ6xRBG-z7kX6QQ")
ADMIN_ID = int(os.getenv("8138159606"))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Hi! Send your message here. Admin will reply you soon.")

@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','document','sticker'])
def handle(m):
    if m.chat.id == ADMIN_ID:
        if m.reply_to_message and m.reply_to_message.forward_from:
            try:
                bot.copy_message(m.reply_to_message.forward_from.id, m.chat.id, m.message_id)
            except:
                bot.send_message(ADMIN_ID, "Please reply on forwarded message.")
    else:
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.send_message(m.chat.id, "Your message has been sent to admin. You will get a reply soon.")

bot.infinity_polling()
