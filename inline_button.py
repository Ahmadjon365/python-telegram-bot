from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from geo_loc import get_location

token = "YOUR_BOT_TOKEN"
admin_id = 00000000

inl_butt = [
    [InlineKeyboardButton(text="Rasm jo'nat", callback_data="send_photo"),
     InlineKeyboardButton(text="Fayl jo'nat", callback_data="send_dock")],
    [InlineKeyboardButton(text="Media jo'nat", callback_data="send_group")],
]

def start_func(update, context):
    # # Bot uchun komandalarni o'zlashtirish
    # commands = [BotCommand(command="start", description="Botni qayta ishga tushirish"),
    #             BotCommand(command="menu", description="Botning menyusiga o'tish"),
    #             BotCommand(command="info", description="Bot haqida ma'lumot")]
    # context.bot.set_my_commands(commands)

    update.message.reply_photo(
        # photo=open("photo.jpg", "rb"),
        photo="https://picsum.photos/1980/1080",
        caption="Assalomu aleykum!", reply_markup=InlineKeyboardMarkup(inl_butt))
    print(update.message.text)
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
        update.message.reply_text(text=f"Sizga ham xayr!")
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


def inl_butt_query(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "send_photo":
        query.message.reply_photo(photo="https://picsum.photos/1900/1000", caption="Random rasm", raply_markup=InlineKeyboardMarkup(inl_butt))
    elif query.data == "send_dock":
        # query.message.reply_document(document=open("dummy.pdf", "rb"), caption="Dummy pdf", raply_markup=InlineKeyboardMarkup(inl_butt))
        query.message.reply_document(document="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                                     caption="Dummy pdf", raply_markup=InlineKeyboardMarkup(inl_butt))
    elif query.data == "send_group":
        query.message.reply_media_group(media=[
            # InputMediaPhoto(media=open("photo.jpg", 'rb')),
            InputMediaPhoto(media=f"https://picsum.photos/{random.randint(1, 30)}/200/300"),
            InputMediaPhoto(media=f"https://picsum.photos/{random.randint(30, 60)}/200/300"),
            InputMediaPhoto(media=f"https://picsum.photos/{random.randint(60, 100)}/200/300"),
        ])


def photo_handler(update, context):
    file = update.message.photo[-1].get_file()
    obj = context.bot.get_file(file)
    obj.download("photos/user_photo.jpg")


def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_func))
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))
    dispatcher.add_handler(CallbackQueryHandler(inl_butt_query))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
