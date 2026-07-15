# ==========================================================
# BB877 Utility Bot
# Version 2.0
# python-telegram-bot 21.10
# ==========================================================

import os
import re
import uuid
import base64
import hashlib
import random
import secrets
import string
import logging

from datetime import datetime

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.constants import ParseMode

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable not found."
    )

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("BB877")

# ==========================================================
# CONVERSATION STATES
# ==========================================================

(
    FANCY_TEXT,

    PASSWORD_GENERATOR,
    PASSWORD_STRENGTH,

    SHA256_HASH,
    BASE64_ENCODE,
    BASE64_DECODE,

    TIMESTAMP,

    TEXT_UPPER,
    TEXT_LOWER,
    TEXT_REVERSE,
    WORD_COUNTER,

    RANDOM_NUMBER,

    GUESS_NUMBER,

) = range(13)

# ==========================================================
# CONSTANTS
# ==========================================================

PASSWORD_SYMBOLS = (
    "!@#$%^&*()"
    "_+-=[]{}"
    "|;:,.<>?"
)

GAME_MIN = 1
GAME_MAX = 100

# ==========================================================
# RANDOM DATA
# ==========================================================

EMOJIS = [

    "😀",
    "😁",
    "😂",
    "🤣",
    "😎",
    "🥳",
    "🤖",
    "🔥",
    "⚡",
    "🎉",
    "🍀",
    "🎯",
    "💎",
    "🚀",
    "❤️",
    "🌈",
    "🐍",
    "🎁",
    "🏆",
    "🍕",

]

QUOTES = [

    "Believe in yourself.",

    "Dream big.",

    "Stay hungry. Stay foolish.",

    "Success is earned.",

    "Consistency beats motivation.",

    "Everything is figureoutable.",

    "Never stop learning.",

    "Small progress is still progress.",

    "Code. Learn. Repeat.",

    "Discipline creates freedom.",

]

logger.info("BB877 Utility Bot initialized.")

# ==========================================================
# KEYBOARDS
# ==========================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "✨ Fancy Text",
                callback_data="fancy",
            )
        ],

        [
            InlineKeyboardButton(
                "🔐 Password Tools",
                callback_data="password",
            )
        ],

        [
            InlineKeyboardButton(
                "🔒 Encoding & Hashing",
                callback_data="encoding",
            )
        ],

        [
            InlineKeyboardButton(
                "📝 Text Tools",
                callback_data="text",
            )
        ],

        [
            InlineKeyboardButton(
                "🎲 Random Tools",
                callback_data="random",
            )
        ],

        [
            InlineKeyboardButton(
                "🎮 Guess Number",
                callback_data="guess",
            )
        ],

        [
            InlineKeyboardButton(
                "❓ Help",
                callback_data="help",
            ),

            InlineKeyboardButton(
                "ℹ About",
                callback_data="about",
            ),
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# ==========================================================
# BACK BUTTON
# ==========================================================

def back_keyboard():

    return InlineKeyboardMarkup(

        [
            [
                InlineKeyboardButton(
                    "⬅ Back to Home",
                    callback_data="home",
                )
            ]
        ]

    )

# ==========================================================
# START
# ==========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 *Welcome to BB877 Utility Bot*\n\n"
        "A production-ready Telegram Utility Bot.\n\n"
        "Choose a tool below."
    )

    if update.callback_query:

        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu(),
        )

    else:

        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu(),
        )

    return ConversationHandler.END


# ==========================================================
# HELP
# ==========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "*BB877 Utility Bot Help*\n\n"

        "Available Tools:\n\n"

        "✨ Fancy Text\n"
        "🔐 Password Generator\n"
        "🛡 Password Strength Checker\n"
        "🔒 SHA-256 Hash\n"
        "📦 Base64 Encode\n"
        "📂 Base64 Decode\n"
        "🆔 UUID Generator\n"
        "🕒 Timestamp Converter\n"
        "🔠 Uppercase\n"
        "🔡 Lowercase\n"
        "↩ Reverse Text\n"
        "📖 Word Counter\n"
        "🎲 Random Number\n"
        "🪙 Coin Flip\n"
        "🎲 Dice\n"
        "😀 Random Emoji\n"
        "💬 Random Quote\n"
        "🎮 Guess Number Game\n\n"

        "Use the buttons to navigate."
    )

    if update.callback_query:

        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END


# ==========================================================
# ABOUT
# ==========================================================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "*BB877 Utility Bot*\n\n"

        "Version: 2.0\n"

        "Framework:\n"
        "python-telegram-bot 21.10\n\n"

        "Deployment:\n"
        "Railway\n\n"

        "Language:\n"
        "Python 3.12"
    )

    if update.callback_query:

        await update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END

# ==========================================================
# MENU SCREENS
# ==========================================================

async def show_password_menu(query):

    await query.edit_message_text(
        text="🔐 *Password Tools*\n\nChoose an option.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔑 Generate Password",
                    callback_data="password_generate",
                )
            ],
            [
                InlineKeyboardButton(
                    "🛡 Password Strength",
                    callback_data="password_strength",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home",
                )
            ],
        ]),
    )


async def show_encoding_menu(query):

    await query.edit_message_text(
        text="🔒 *Encoding & Hashing*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "SHA-256",
                    callback_data="sha256",
                )
            ],
            [
                InlineKeyboardButton(
                    "Base64 Encode",
                    callback_data="b64_encode",
                )
            ],
            [
                InlineKeyboardButton(
                    "Base64 Decode",
                    callback_data="b64_decode",
                )
            ],
            [
                InlineKeyboardButton(
                    "UUID Generator",
                    callback_data="uuid",
                )
            ],
            [
                InlineKeyboardButton(
                    "Timestamp",
                    callback_data="timestamp",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home",
                )
            ],
        ]),
    )


async def show_text_menu(query):

    await query.edit_message_text(
        text="📝 *Text Tools*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔠 Uppercase",
                    callback_data="upper",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔡 Lowercase",
                    callback_data="lower",
                )
            ],
            [
                InlineKeyboardButton(
                    "↩ Reverse Text",
                    callback_data="reverse",
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 Word Counter",
                    callback_data="words",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home",
                )
            ],
        ]),
    )


async def show_random_menu(query):

    await query.edit_message_text(
        text="🎲 *Random Tools*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎲 Random Number",
                    callback_data="random_number",
                )
            ],
            [
                InlineKeyboardButton(
                    "🪙 Coin Flip",
                    callback_data="coin",
                )
            ],
            [
                InlineKeyboardButton(
                    "🎲 Roll Dice",
                    callback_data="dice",
                )
            ],
            [
                InlineKeyboardButton(
                    "😀 Random Emoji",
                    callback_data="emoji",
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Random Quote",
                    callback_data="quote",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home",
                )
            ],
        ]),
    )

# ==========================================================
# CALLBACK ROUTER
# ==========================================================

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ---------------- HOME ----------------

    if data == "home":
        return await start(update, context)

    # ---------------- HELP ----------------

    elif data == "help":
        return await help_command(update, context)

    # ---------------- ABOUT ----------------

    elif data == "about":
        return await about(update, context)

    # ---------------- PASSWORD MENU ----------------

    elif data == "password":
        await show_password_menu(query)
        return ConversationHandler.END

    elif data == "password_generate":
        await query.edit_message_text(
            "🔑 Enter password length (4-128):",
            reply_markup=back_keyboard(),
        )
        return PASSWORD_GENERATOR

    elif data == "password_strength":
        await query.edit_message_text(
            "🛡 Send the password to check:",
            reply_markup=back_keyboard(),
        )
        return PASSWORD_STRENGTH

    # ---------------- ENCODING MENU ----------------

    elif data == "encoding":
        await show_encoding_menu(query)
        return ConversationHandler.END

    elif data == "sha256":
        await query.edit_message_text(
            "🔒 Send text to hash:",
            reply_markup=back_keyboard(),
        )
        return SHA256_HASH

    elif data == "b64_encode":
        await query.edit_message_text(
            "📦 Send text to Base64 encode:",
            reply_markup=back_keyboard(),
        )
        return BASE64_ENCODE

    elif data == "b64_decode":
        await query.edit_message_text(
            "📦 Send Base64 text to decode:",
            reply_markup=back_keyboard(),
        )
        return BASE64_DECODE

    elif data == "uuid":
        return await uuid_handler(update, context)

    elif data == "timestamp":
        await query.edit_message_text(
            "🕒 Send a Unix timestamp:",
            reply_markup=back_keyboard(),
        )
        return TIMESTAMP

    # ---------------- TEXT MENU ----------------

    elif data == "text":
        await show_text_menu(query)
        return ConversationHandler.END

    elif data == "upper":
        await query.edit_message_text(
            "🔠 Send text:",
            reply_markup=back_keyboard(),
        )
        return TEXT_UPPER

    elif data == "lower":
        await query.edit_message_text(
            "🔡 Send text:",
            reply_markup=back_keyboard(),
        )
        return TEXT_LOWER

    elif data == "reverse":
        await query.edit_message_text(
            "↩ Send text:",
            reply_markup=back_keyboard(),
        )
        return TEXT_REVERSE

    elif data == "words":
        await query.edit_message_text(
            "📖 Send text:",
            reply_markup=back_keyboard(),
        )
        return WORD_COUNTER

    # ---------------- RANDOM MENU ----------------

    elif data == "random":
        await show_random_menu(query)
        return ConversationHandler.END

    elif data == "random_number":
        await query.edit_message_text(
            "🎲 Send minimum and maximum.\n\nExample:\n1 100",
            reply_markup=back_keyboard(),
        )
        return RANDOM_NUMBER

    elif data == "coin":
        return await coin_flip_handler(update, context)

    elif data == "dice":
        return await dice_handler(update, context)

    elif data == "emoji":
        return await random_emoji_handler(update, context)

    elif data == "quote":
        return await random_quote_handler(update, context)

    # ---------------- GUESS GAME ----------------

    elif data == "guess":

        context.user_data["guess_number"] = random.randint(
            GAME_MIN,
            GAME_MAX,
        )

        context.user_data["attempts"] = 0

        await query.edit_message_text(
            f"🎮 I'm thinking of a number between {GAME_MIN} and {GAME_MAX}.\n\nSend your guess.",
            reply_markup=back_keyboard(),
        )

        return GUESS_NUMBER

    # ---------------- FANCY TEXT ----------------

    elif data == "fancy":
        await query.edit_message_text(
            "✨ Send the text you want to convert:",
            reply_markup=back_keyboard(),
        )
        return FANCY_TEXT

    return ConversationHandler.END

# ==========================================================
# PASSWORD GENERATOR
# ==========================================================

async def password_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if not text.isdigit():

        await update.message.reply_text(
            "❌ Please enter a number between 4 and 128.",
            reply_markup=back_keyboard(),
        )
        return PASSWORD_GENERATOR

    length = int(text)

    if length < 4 or length > 128:

        await update.message.reply_text(
            "❌ Password length must be between 4 and 128.",
            reply_markup=back_keyboard(),
        )
        return PASSWORD_GENERATOR

    chars = (
        string.ascii_letters
        + string.digits
        + PASSWORD_SYMBOLS
    )

    password = "".join(
        secrets.choice(chars)
        for _ in range(length)
    )

    await update.message.reply_text(
        f"🔑 *Generated Password*\n\n`{password}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# PASSWORD STRENGTH
# ==========================================================

async def password_strength(update: Update, context: ContextTypes.DEFAULT_TYPE):

    password = update.message.text

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(rf"[{re.escape(PASSWORD_SYMBOLS)}]", password):
        score += 1

    if score <= 1:
        strength = "🔴 Very Weak"

    elif score == 2:
        strength = "🟠 Weak"

    elif score == 3:
        strength = "🟡 Medium"

    elif score == 4:
        strength = "🟢 Strong"

    else:
        strength = "💪 Very Strong"

    await update.message.reply_text(
        f"🛡 *Password Strength*\n\n{strength}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# SHA-256
# ==========================================================

async def sha256_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    digest = hashlib.sha256(
        update.message.text.encode("utf-8")
    ).hexdigest()

    await update.message.reply_text(
        f"🔒 *SHA-256*\n\n`{digest}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END

    # ==========================================================
# BASE64 ENCODE
# ==========================================================

async def base64_encode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    encoded = base64.b64encode(
        text.encode("utf-8")
    ).decode("utf-8")

    await update.message.reply_text(
        f"📦 *Base64 Encoded*\n\n`{encoded}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# BASE64 DECODE
# ==========================================================

async def base64_decode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        decoded = base64.b64decode(
            update.message.text
        ).decode("utf-8")

        await update.message.reply_text(
            f"📂 *Decoded Text*\n\n{decoded}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    except Exception:

        await update.message.reply_text(
            "❌ Invalid Base64 text.",
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END


# ==========================================================
# UUID GENERATOR
# ==========================================================

async def uuid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    new_uuid = str(uuid.uuid4())

    await update.callback_query.edit_message_text(
        f"🆔 *UUID v4*\n\n`{new_uuid}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# TIMESTAMP CONVERTER
# ==========================================================

async def timestamp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        ts = int(update.message.text)

        dt = datetime.fromtimestamp(ts)

        await update.message.reply_text(
            f"🕒 *Date & Time*\n\n`{dt}`",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    except ValueError:

        await update.message.reply_text(
            "❌ Invalid Unix timestamp.",
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END

# ==========================================================
# UPPERCASE
# ==========================================================

async def uppercase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.reply_text(
        text.upper(),
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# LOWERCASE
# ==========================================================

async def lowercase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.reply_text(
        text.lower(),
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# REVERSE TEXT
# ==========================================================

async def reverse_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.reply_text(
        text[::-1],
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# WORD COUNTER
# ==========================================================

async def word_counter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    words = len(text.split())

    chars = len(text)

    lines = len(text.splitlines())

    result = (
        "📖 *Word Counter*\n\n"
        f"Words : `{words}`\n"
        f"Characters : `{chars}`\n"
        f"Lines : `{lines}`"
    )

    await update.message.reply_text(
        result,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END

# ==========================================================
# FANCY TEXT FONTS
# ==========================================================

NORMAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
FONTS = {

"𝗕𝗼𝗹𝗱":
"𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
"𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇",

"𝘐𝘵𝘢𝘭𝘪𝘤":
"𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
"𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",

"𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘":
"𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"
"𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯",

"𝙼𝚘𝚗𝚘":
"𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
"𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣",

"𝔻𝕠𝕦𝕓𝕝𝕖":
"𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
"𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫",

}

# ==========================================================
# FANCY TEXT ENGINE
# ==========================================================

def convert_font(text: str, alphabet: str):

    result = ""

    for letter in text:

        index = NORMAL.find(letter)

        if index == -1:
            result += letter

        else:
            result += alphabet[index]

    return result


# ==========================================================
# FANCY TEXT HANDLER
# ==========================================================

async def fancy_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    results = []

    for font_name, alphabet in FONTS.items():

        try:

            converted = convert_font(
                text,
                alphabet,
            )

            results.append(
                f"*{font_name}*\n`{converted}`"
            )

        except Exception:

            continue

    if not results:

        await update.message.reply_text(
            "❌ Unable to convert text.",
            reply_markup=back_keyboard(),
        )

        return ConversationHandler.END

    message = "\n\n".join(results)

    if len(message) > 4000:
        message = message[:3900] + "\n\n..."

    await update.message.reply_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END

# ==========================================================
# RANDOM NUMBER
# ==========================================================

async def random_number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        parts = update.message.text.split()

        if len(parts) != 2:
            raise ValueError

        minimum = int(parts[0])
        maximum = int(parts[1])

        if minimum > maximum:
            minimum, maximum = maximum, minimum

        number = random.randint(minimum, maximum)

        await update.message.reply_text(
            f"🎲 Random Number\n\n**{number}**",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_keyboard(),
        )

    except Exception:

        await update.message.reply_text(
            "❌ Example:\n\n1 100",
            reply_markup=back_keyboard(),
        )

        return RANDOM_NUMBER

    return ConversationHandler.END


# ==========================================================
# COIN FLIP
# ==========================================================

async def coin_flip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    result = random.choice(["🪙 Heads", "🪙 Tails"])

    await update.callback_query.edit_message_text(
        f"*Coin Flip*\n\n{result}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# DICE
# ==========================================================

async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    value = random.randint(1, 6)

    await update.callback_query.edit_message_text(
        f"🎲 Dice Roll\n\n**{value}**",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# RANDOM EMOJI
# ==========================================================

async def random_emoji_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    emoji = random.choice(EMOJIS)

    await update.callback_query.edit_message_text(
        f"😀 Random Emoji\n\n{emoji}",
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# RANDOM QUOTE
# ==========================================================

async def random_quote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    quote = random.choice(QUOTES)

    await update.callback_query.edit_message_text(
        f"💬 Quote\n\n_{quote}_",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# GUESS NUMBER GAME
# ==========================================================

async def guess_number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        guess = int(update.message.text)

    except ValueError:

        await update.message.reply_text(
            "❌ Enter a valid number.",
            reply_markup=back_keyboard(),
        )

        return GUESS_NUMBER

    target = context.user_data.get("guess_number")

    attempts = context.user_data.get("attempts", 0) + 1

    context.user_data["attempts"] = attempts

    if guess < target:

        await update.message.reply_text(
            "📉 Too low!",
            reply_markup=back_keyboard(),
        )

        return GUESS_NUMBER

    if guess > target:

        await update.message.reply_text(
            "📈 Too high!",
            reply_markup=back_keyboard(),
        )

        return GUESS_NUMBER

    await update.message.reply_text(
        f"🎉 Correct!\n\nAttempts: {attempts}",
        reply_markup=back_keyboard(),
    )

    context.user_data.pop("guess_number", None)
    context.user_data.pop("attempts", None)

    return ConversationHandler.END

# ==========================================================
# MAIN
# ==========================================================

def main():

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(callback_router),
        ],

        states={

            PASSWORD_GENERATOR: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    password_generator,
                )
            ],

            PASSWORD_STRENGTH: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    password_strength,
                )
            ],

            SHA256_HASH: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    sha256_handler,
                )
            ],

            BASE64_ENCODE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    base64_encode_handler,
                )
            ],

            BASE64_DECODE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    base64_decode_handler,
                )
            ],

            TIMESTAMP: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    timestamp_handler,
                )
            ],

            TEXT_UPPER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    uppercase_handler,
                )
            ],

            TEXT_LOWER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    lowercase_handler,
                )
            ],

            TEXT_REVERSE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    reverse_text_handler,
                )
            ],

            WORD_COUNTER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    word_counter_handler,
                )
            ],

            RANDOM_NUMBER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    random_number_handler,
                )
            ],

            GUESS_NUMBER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    guess_number_handler,
                )
            ],

            FANCY_TEXT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    fancy_text_handler,
                )
            ],

        },

        fallbacks=[
            CommandHandler("start", start),
        ],

        allow_reentry=True,
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    application.add_handler(conv_handler)

    application.run_polling()


# ==========================================================
# START BOT
# ==========================================================

if __name__ == "__main__":
    main()
