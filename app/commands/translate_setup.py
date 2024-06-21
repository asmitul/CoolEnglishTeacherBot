import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

# logger
from logger import setup_logger
logger = setup_logger()

from configs.telegram import DEVELOPER_ID

user_selections = {}

CONFIG_FILE = 'user_config.json'

def save_config():
    # Convert sets to lists for JSON serialization
    serializable_selections = {user_id: list(selections) for user_id, selections in user_selections.items()}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(serializable_selections, f)

def load_config():
    global user_selections
    try:
        with open(CONFIG_FILE, 'r') as f:
            serializable_selections = json.load(f)
            # Convert lists back to sets
            user_selections = {int(user_id): set(selections) for user_id, selections in serializable_selections.items()}
    except FileNotFoundError:
        user_selections = {}

async def translate_setup(update: Update, context: CallbackContext) -> None:
    load_config()
    keyboard = generate_keyboard(update.message.from_user.id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

async def translate_setup_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_selections:
        user_selections[user_id] = set()

    await query.answer()

    if query.data == 'done':
        selected_options = user_selections.get(user_id, set())
        await query.edit_message_text(text=f"Selected options: {', '.join(selected_options) if selected_options else 'None'}")

        # Save selected options to local config file
        save_config()
    else:
        if query.data in user_selections[user_id]:
            user_selections[user_id].remove(query.data)
        else:
            user_selections[user_id].add(query.data)
        reply_markup = InlineKeyboardMarkup(generate_keyboard(user_id))
        await query.edit_message_reply_markup(reply_markup=reply_markup)

def generate_keyboard(user_id):
    keyboard = [
        [InlineKeyboardButton("Select Source Language 🌐", callback_data='useless')],
        [
            InlineKeyboardButton("Chinese🇨🇳", callback_data='source_language_Chinese'),
            InlineKeyboardButton("English🇺🇸", callback_data='source_language_English'),
            InlineKeyboardButton("Turkish🇹🇷", callback_data='source_language_Turkish'),
        ],
        [InlineKeyboardButton("Select Target Language 🎯", callback_data='useless')],
        [
            InlineKeyboardButton("Chinese🇨🇳", callback_data='target_language_Chinese'),
            InlineKeyboardButton("English🇺🇸", callback_data='target_language_English'),
            InlineKeyboardButton("Turkish🇹🇷", callback_data='target_language_Turkish'),
        ],
        [InlineKeyboardButton("Select Audio Language 🔊", callback_data='useless')],
        [
            InlineKeyboardButton("Source", callback_data='audio_language_source'),
            InlineKeyboardButton("Target", callback_data='audio_language_target'),
        ],
        [InlineKeyboardButton("Select Voice 👤", callback_data='useless')],
        [
            InlineKeyboardButton("alloy", callback_data='voice_alloy'),
            InlineKeyboardButton("echo", callback_data='voice_echo'),
            InlineKeyboardButton("fable", callback_data='voice_fable'),
        ],
        [
            InlineKeyboardButton("onyx", callback_data='voice_onyx'),
            InlineKeyboardButton("nova", callback_data='voice_nova'),
            InlineKeyboardButton("shimmer", callback_data='voice_shimmer'),
        ],
        [InlineKeyboardButton("Speed factor ⏩", callback_data='useless')],
        [
            InlineKeyboardButton("Slow🐢", callback_data='speed_factor_0.75'),
            InlineKeyboardButton("Normal", callback_data='speed_factor_1'),
            InlineKeyboardButton("Quick🚀", callback_data='speed_factor_1.25'),
        ],
        [InlineKeyboardButton("Done ✅", callback_data='done')]
    ]
    
    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            if button.callback_data in user_selections.get(user_id, set()):
                text = f"✅ {text}"
            new_row.append(InlineKeyboardButton(text, callback_data=button.callback_data))
        new_keyboard.append(new_row)
    
    return new_keyboard

