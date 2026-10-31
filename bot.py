import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Welcome! Message koro, admin tomay reply debe.")

@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','document','sticker'])
def handle(m):
    if m.chat.id == ADMIN_ID:
        if m.reply_to_message and m.reply_to_message.forward_from:
            bot.copy_message(m.reply_to_message.forward_from.id, m.chat.id, m.message_id)
    else:
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.send_message(m.chat.id, "Done! Admin ke pathiye diyechi.")

bot.infinity_polling()
