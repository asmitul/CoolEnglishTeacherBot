from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters,ContextTypes

from configs.telegram import TOKEN
from error.handler import handler as error_handler
from commands.translate_setup import translate_setup, translate_setup_button
# from commands.translate import translate, translate_text_handler, TEXT, translate_cancel
from commands.translate_direct import translate_text_handler_direct

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("translate_setup", translate_setup))
    application.add_handler(CallbackQueryHandler(translate_setup_button))

    # Add conversation handler
    # translate_conversation_handler = ConversationHandler(
    #     entry_points=[CommandHandler('translate', translate)],
    #     states={
    #         TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text_handler)],
    #     },
    #     fallbacks=[CommandHandler('cancel', translate_cancel)],
    # )

    # application.add_handler(translate_conversation_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text_handler_direct))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()