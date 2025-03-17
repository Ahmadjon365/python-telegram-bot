from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from geo_loc import get_location

token = "7688427772:AAEQTKMp3DqIEizhN5fvqBbsGd7oPI8Jjmg"
admin_id = 92091371

def start_func(update, context):
    update.message.reply_text(text="Assalomu aleykum!")
    print(update.message.text)
    # print(context.bot)
    print(update.message.from_user)

def menu(update, context):
    buttons = [
        [KeyboardButton("📞 Raqam yuborish", request_contact=True), KeyboardButton("📷 Manzil yuborish", request_location=True)],
        [KeyboardButton("Menu 3"), KeyboardButton("Menu 4")],]

    update.message.reply_text(
        text="Iltimos, kerakli bo'limni tanlang:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

def message_handler(update, context):
    message = update.message.text
    print(message)
    if message == "Assalomu aleykum":
        update.message.reply_text(text=f"Va aleykum assalom!")
    elif message == "Xayr":
        update.message.reply_text(text=f"Sizga ham xayr")
    elif message == "Nima gaplar o'zi?":
        update.message.reply_text(text=f"Hech gap yo'q, sizda nima gaplar?")
    else:
        update.message.reply_text(text=message)


def contact_handler(update, context):
    phone_number = update.message.contact.phone_number
    # update.message.reply_text(text=f"Sizning nomeringiz '{phone_number}'")
    context.bot.send_message(chat_id=admin_id, text=f"yangi foydalanuvchi raqami: {phone_number}")


def location_handler(update, context):
    location = update.message.location
    # update.message.reply_location(latitude=location.latitude, longitude=location.longitude)
    context.bot.send_location(chat_id=admin_id, latitude=location.latitude, longitude=location.longitude)
    update.message.reply_text(text=f"latitude={location.latitude}, longitude={location.longitude}")
    address = get_location(location.latitude, location.longitude)
    update.message.reply_text(text=f"Manzil: {address}")

# def poll_handler(update, context):
#     poll = update.message.poll
#     context.bot.send_poll(chat_id=admin_id, question=poll.question, options=poll.options)


def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_func))
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))
    # dispatcher.add_handler(MessageHandler(Filters.poll, poll_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
