import logging
from ptb_1 import token, admin_id
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import sqlite3
from geo_loc import get_location

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

connection = sqlite3.connect("users.db")
cursor = connection.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
               phone_number TEXT PRIMARY KEY,
               first_name TEXT,
               last_name TEXT,
               age INTEGER,
               gender TEXT,
               location TEXT,
               latitude REAL,
               longitude REAL)
""")
connection.commit()

def start(update, context):
    reply_text = "Assalomu aleykum! Telefon raqam kiriting:"
    reply_murkup = ReplyKeyboardMarkup([[KeyboardButton("📞 Raqam yuborish", request_contact=True)]],
                                       resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, reply_markup=reply_murkup)
    logging.info(f"User - {update.effective_chat.id} started registration!")
    return 'PHONE_NUMBER'


def phone_number(update, context):
    phone_num = update.message.contact.phone_number
    context.user_data['phone_number'] = phone_num
    update.message.reply_text("Ismingizni nima:")
    return 'FIRST_NAME'


def first_name(update, context):
    first_name = update.message.text
    context.user_data['first_name'] = first_name
    update.message.reply_text("Familiyangizni nima:")
    return 'LAST_NAME'


def last_name(update, context):
    last_name = update.message.text
    context.user_data['last_name'] = last_name
    update.message.reply_text("Yoshingizni kiriting:")
    return 'AGE'


def age(update, context):
    age = update.message.text
    context.user_data['age'] = age
    update.message.reply_text("Jinsingizni tanlang:", reply_markup=ReplyKeyboardMarkup([['Erkak', 'Ayol']], resize_keyboard=True, one_time_keyboard=True))
    return 'GENDER'


def gender(update, context):
    gender = update.message.text
    context.user_data['gender'] = gender
    reply_text = "Manzilingizni yuboring:"
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton(text="📍 Geolokatsiya", request_location=True)]], 
        resize_keyboard=True, 
        one_time_keyboard=True
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text,
                             reply_markup=reply_markup)
    return 'GEOLOCATION'


def geolocation(update, context):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    address = get_location(latitude, longitude)

    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude
    context.user_data['address'] = address

    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (
            context.user_data['phone_number'],
            context.user_data['first_name'],
            context.user_data['last_name'],
            context.user_data['age'],
            context.user_data['gender'],
            context.user_data['address'],
            context.user_data['latitude'],
            context.user_data['longitude'],
        ))
        connection.commit()
    except Exception as e:
        logging.error(f"Database error: {e}")
        update.message.reply_text("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")
        return ConversationHandler.END
    finally:
        cursor.close()
        connection.close()

    logging.info("User registered")

    # ✅ `reply_text` orqali bot to‘g‘ri javob qaytaradi
    update.message.reply_text("Ma'lumotlar saqlandi, rahmat!")
    
    # ✅ To‘g‘ri formatlangan javob qaytarish
    user_data = context.user_data
    reply_markup=ReplyKeyboardMarkup(
        [[KeyboardButton(text="/start")]], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"""Sizning ma'lumotlaringiz:
📞 Telefon: {user_data['phone_number']}
👤 Ism: {user_data['first_name']}
🆔 Familiya: {user_data['last_name']}
🔢 Yosh: {user_data['age']}
🚻 Jins: {user_data['gender']}
📍 Manzil: {user_data['address']}
    """, reply_markup=reply_markup)

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text("Bekor qilindi!")
    return ConversationHandler.END


def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'PHONE_NUMBER': [MessageHandler(Filters.contact & ~Filters.command, phone_number)],
            'FIRST_NAME': [MessageHandler(Filters.text & ~Filters.command, first_name)],
            'LAST_NAME': [MessageHandler(Filters.text & ~Filters.command, last_name)],
            'AGE': [MessageHandler(Filters.text & ~Filters.command, age)],
            'GENDER': [MessageHandler(Filters.text & ~Filters.command, gender)],
            'GEOLOCATION': [MessageHandler(Filters.location & ~Filters.command, geolocation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)])

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
