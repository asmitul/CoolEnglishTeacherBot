import json
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# logger
from logger import setup_logger
logger = setup_logger()

from API import translate_text, download_audio_file

user_selections = {}

CONFIG_FILE = 'user_config.json'

def load_config():
    global user_selections
    try:
        with open(CONFIG_FILE, 'r') as f:
            serializable_selections = json.load(f)
            # Convert lists back to sets
            user_selections = {int(user_id): set(selections) for user_id, selections in serializable_selections.items()}
    except FileNotFoundError:
        user_selections = {}



async def translate_text_handler_direct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    chat_id = update.message.chat_id
    load_config()

    user_config = user_selections.get(chat_id)
    if user_config:
        pass
    else:
        await context.bot.send_message(chat_id, f"Please setup first: /translate_setup")
        return


    source_language = extract_value(user_config, 'source_language_')
    target_language = extract_value(user_config, 'target_language_')
    audio_language = extract_value(user_config, 'audio_language_')
    voice = extract_value(user_config, 'voice_')
    try:
        speed_factor = float(extract_value(user_config, 'speed_factor_'))
    except ValueError:
        speed_factor = 1.0

    translated_text = translate_text(text, source_language, target_language, audio_language, voice, speed_factor)

    await update.message.reply_text(translated_text['translated_text'])

    if 'file_id' in translated_text:
        audio_file = translated_text['file_id']
        download_audio_file(audio_file, 'downloaded_speech.mp3')


        await update.message.reply_voice(voice=open('downloaded_speech.mp3', 'rb'))


def extract_value(s, prefix):
    for item in s:
        if item.startswith(prefix):
            return item[len(prefix):]