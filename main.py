import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import filters, MessageHandler, ApplicationBuilder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# bot should only work on this chat
THE_GROUPS_CHAT_ID = -1001830793456  # this is a random number


async def listen_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Listen to all msgs and filter for left chat member requests
    """
    # print(update)

    if update.effective_chat.type == "group" or "supergroup":
        if update.effective_chat.id == THE_GROUPS_CHAT_ID:

            # deleting chat member left service msg
            if update.message.left_chat_member is not None:
                who_left = update.message.left_chat_member.id
                await context.bot.ban_chat_member(update.effective_chat.id, who_left)
                await context.bot.delete_message(update.effective_chat.id, update.message.message_id)


if __name__ == '__main__':
    token = "5544541078:AAHiZ03MPNt60qMlPqH9efqRGOJ3DFQK_LM"
    application = ApplicationBuilder().token(token).build()

    main_h = MessageHandler(filters=filters.ALL, callback=listen_all)

    application.add_handler(main_h)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
