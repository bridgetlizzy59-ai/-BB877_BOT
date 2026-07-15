import os
import re
import uuid
import base64
import hashlib
import random
import string
import logging
from datetime import datetime
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found!")

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("BB877")

# ==========================================================
# STATES
# ==========================================================

(
    FANCY_TEXT,
    PASSWORD_GEN,
    PASSWORD_STRENGTH,
    SHA256_HASH,
    BASE64_ENCODE,
    BASE64_DECODE,
    UUID_GEN,
    TIMESTAMP,
    TO_UPPER,
    TO_LOWER,
    REVERSE_TEXT,
    WORD_COUNTER,
    RANDOM_NUMBER,
    COIN_FLIP,
    DICE,
    RANDOM_EMOJI,
    RANDOM_QUOTE,
    GUESS_GAME,
) = range(18)

# ==========================================================
# USER DATA
# ==========================================================

guess_numbers = {}

# ==========================================================
# KEYBOARDS
# ==========================================================


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton("✨ Fancy Text", callback_data="fancy"),
            InlineKeyboardButton("🔐 Password", callback_data="password"),
        ],

        [
            InlineKeyboardButton("🛡 Strength", callback_data="strength"),
            InlineKeyboardButton("🔑 SHA256", callback_data="sha256"),
        ],

        [
            InlineKeyboardButton("📦 Base64", callback_data="base64"),
            InlineKeyboardButton("🆔 UUID", callback_data="uuid"),
        ],

        [
            InlineKeyboardButton("⏰ Timestamp", callback_data="timestamp"),
            InlineKeyboardButton("🔠 Uppercase", callback_data="upper"),
        ],

        [
            InlineKeyboardButton("🔡 Lowercase", callback_data="lower"),
            InlineKeyboardButton("🔄 Reverse", callback_data="reverse"),
        ],

        [
            InlineKeyboardButton("📖 Word Count", callback_data="word"),
            InlineKeyboardButton("🎲 Random", callback_data="random"),
        ],

        [
            InlineKeyboardButton("🪙 Coin", callback_data="coin"),
            InlineKeyboardButton("🎲 Dice", callback_data="dice"),
        ],

        [
            InlineKeyboardButton("😀 Emoji", callback_data="emoji"),
            InlineKeyboardButton("💬 Quote", callback_data="quote"),
        ],

        [
            InlineKeyboardButton("🎮 Guess Game", callback_data="guess"),
        ],

        [
            InlineKeyboardButton("ℹ Help", callback_data="help"),
            InlineKeyboardButton("👤 About", callback_data="about"),
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


def back_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="back",
                )
            ]
        ]
    )

# ==========================================================
# START
# ==========================================================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Welcome to *BB877 Utility Bot*\n\n"
        "Choose any tool below."
    )

    if update.message:

        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    else:

        await update.callback_query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

# ==========================================================
# HELP
# ==========================================================


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📚 BB877 Utility Bot

Available Tools

✨ Fancy Text
🔐 Password Generator
🛡 Password Strength
🔑 SHA256
📦 Base64 Encode
📦 Base64 Decode
🆔 UUID Generator
⏰ Timestamp
🔠 Uppercase
🔡 Lowercase
🔄 Reverse Text
📖 Word Counter
🎲 Random Number
🪙 Coin Flip
🎲 Dice
😀 Random Emoji
💬 Random Quote
🎮 Guess Number

Use the menu below.
"""

    if update.message:

        await update.message.reply_text(
            text,
            reply_markup=back_keyboard(),
        )

    else:

        await update.callback_query.edit_message_text(
            text,
            reply_markup=back_keyboard(),
        )

# ==========================================================
# ABOUT
# ==========================================================


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🤖 BB877 Utility Bot\n\n"
        "Version : 1.0\n"
        "Framework : python-telegram-bot 21.10\n"
        "Deployment : Railway\n"
        "Language : Python 3.12\n\n"
        "Made for productivity."
    )

    if update.message:

        await update.message.reply_text(
            text,
            reply_markup=back_keyboard(),
        )

    else:

        await update.callback_query.edit_message_text(
            text,
            reply_markup=back_keyboard(),
        )

# ==========================================================
# CALLBACK ROUTER
# ==========================================================


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    logger.info("Button clicked: %s", data)

    if data == "back":

        return await start(update, context)

    elif data == "help":

        return await help_command(update, context)

    elif data == "about":

        return await about(update, context)

    elif data == "fancy":

        await query.edit_message_text(
            "Send the text you want to convert into Fancy Text.",
            reply_markup=back_keyboard(),
        )

        return FANCY_TEXT

    elif data == "password":

        await query.edit_message_text(
            "Send desired password length (Example: 16)",
            reply_markup=back_keyboard(),
        )

        return PASSWORD_GEN

    elif data == "strength":

        await query.edit_message_text(
            "Send a password to check its strength.",
            reply_markup=back_keyboard(),
        )

        return PASSWORD_STRENGTH

    elif data == "sha256":

        await query.edit_message_text(
            "Send text to hash using SHA-256.",
            reply_markup=back_keyboard(),
        )

        return SHA256_HASH

    elif data == "base64":

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Encode",
                        callback_data="b64_encode",
                    ),
                    InlineKeyboardButton(
                        "Decode",
                        callback_data="b64_decode",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="back",
                    )
                ],
            ]
        )

        await query.edit_message_text(
            "Choose Base64 operation.",
            reply_markup=keyboard,
        )

    elif data == "b64_encode":

        await query.edit_message_text(
            "Send text to Base64 Encode.",
            reply_markup=back_keyboard(),
        )

        return BASE64_ENCODE

    elif data == "b64_decode":

        await query.edit_message_text(
            "Send Base64 text to Decode.",
            reply_markup=back_keyboard(),
        )

        return BASE64_DECODE

    elif data == "uuid":

        return UUID_GEN

    elif data == "timestamp":

        await query.edit_message_text(
            "Send Unix timestamp.",
            reply_markup=back_keyboard(),
        )

        return TIMESTAMP

    elif data == "upper":

        await query.edit_message_text(
            "Send text.",
            reply_markup=back_keyboard(),
        )

        return TO_UPPER

    elif data == "lower":

        await query.edit_message_text(
            "Send text.",
            reply_markup=back_keyboard(),
        )

        return TO_LOWER

    elif data == "reverse":

        await query.edit_message_text(
            "Send text.",
            reply_markup=back_keyboard(),
        )

        return REVERSE_TEXT

    elif data == "word":

        await query.edit_message_text(
            "Send text.",
            reply_markup=back_keyboard(),
        )

        return WORD_COUNTER

    elif data == "random":

        await query.edit_message_text(
            "Send two numbers.\n\nExample:\n1 100",
            reply_markup=back_keyboard(),
        )

        return RANDOM_NUMBER

    elif data == "coin":

        return COIN_FLIP

    elif data == "dice":

        return DICE

    elif data == "emoji":

        return RANDOM_EMOJI

    elif data == "quote":

        return RANDOM_QUOTE

  elif data == "guess":

    return await guess_game_start(update, context)

# ==========================================================
# PART 1 END
# ==========================================================
# ==========================================================
# FANCY TEXT (20+ FONTS)
# ==========================================================

FONTS = [
    str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻0123456789"
    ),
    str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛0123456789"
    ),
]

FONT_NAMES = [
    "Italic",
    "Bold Italic",
]

UNICODE_STYLES = [
    ("𝔸","𝔹","ℂ","𝔻","𝔼","𝔽","𝔾","ℍ","𝕀","𝕁","𝕂","𝕃","𝕄","ℕ","𝕆","ℙ","ℚ","ℝ","𝕊","𝕋","𝕌","𝕍","𝕎","𝕏","𝕐","ℤ"),
    ("🄰","🄱","🄲","🄳","🄴","🄵","🄶","🄷","🄸","🄹","🄺","🄻","🄼","🄽","🄾","🄿","🅀","🅁","🅂","🅃","🅄","🅅","🅆","🅇","🅈","🅉"),
]

EMBELLISH = [
    lambda t: "✨ " + t + " ✨",
    lambda t: "🔥 " + t + " 🔥",
    lambda t: "💎 " + t + " 💎",
    lambda t: "❤️ " + t + " ❤️",
    lambda t: "🌸 " + t + " 🌸",
    lambda t: "⚡ " + t + " ⚡",
    lambda t: "👑 " + t + " 👑",
    lambda t: "🎀 " + t + " 🎀",
    lambda t: "🦋 " + t + " 🦋",
    lambda t: "🌟 " + t + " 🌟",
]


def bubble(text):
    out = ""
    for c in text.upper():
        if "A" <= c <= "Z":
            out += chr(0x1F150 + ord(c)-65)
        else:
            out += c
    return out


def double_struck(text):
    normal="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy="𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"
    table=str.maketrans(normal,fancy)
    return text.translate(table)


def monospace(text):
    normal="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy="𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"
    table=str.maketrans(normal,fancy)
    return text.translate(table)


def bold(text):
    normal="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy="𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    table=str.maketrans(normal,fancy)
    return text.translate(table)


def italic(text):
    normal="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy="𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"
    table=str.maketrans(normal,fancy)
    return text.translate(table)


async def fancy_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    results = []

    results.append(f"**Original**\n{text}\n")

    results.append(f"**Bold**\n{bold(text)}")
    results.append(f"**Italic**\n{italic(text)}")
    results.append(f"**Double Struck**\n{double_struck(text)}")
    results.append(f"**Monospace**\n{monospace(text)}")
    results.append(f"**Bubble**\n{bubble(text)}")

    for i, func in enumerate(EMBELLISH, start=1):
        results.append(f"**Style {i}**\n{func(text)}")

    results.append(f"`{text}`")
    results.append(f"||{text}||")
    results.append(text.upper())
    results.append(text.lower())
    results.append(" ".join(text))
    results.append("•".join(text))
    results.append("-".join(text))
    results.append("_".join(text))
    results.append("★ " + text + " ★")
    results.append("✿ " + text + " ✿")
    results.append("➜ " + text)
    results.append("☞ " + text)
    results.append("❖ " + text)

    await update.message.reply_text(
        "\n\n".join(results),
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END
    # ==========================================================
# PASSWORD GENERATOR
# ==========================================================

SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?/"

async def password_generator_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    try:
        length = int(text)
    except ValueError:
        await update.message.reply_text(
            "❌ Please send a valid number.\nExample: 16",
            reply_markup=back_keyboard(),
        )
        return PASSWORD_GEN

    if length < 4 or length > 128:
        await update.message.reply_text(
            "⚠️ Password length must be between 4 and 128.",
            reply_markup=back_keyboard(),
        )
        return PASSWORD_GEN

    chars = (
        string.ascii_letters
        + string.digits
        + SPECIAL_CHARACTERS
    )

    while True:
        password = "".join(random.choice(chars) for _ in range(length))

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in SPECIAL_CHARACTERS for c in password)
        ):
            break

    await update.message.reply_text(
        f"🔐 Generated Password\n\n`{password}`",
        parse_mode="Markdown",
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# PASSWORD STRENGTH CHECKER
# ==========================================================

def calculate_password_strength(password: str):

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if len(password) >= 12:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    if score <= 2:
        level = "🔴 Weak"

    elif score <= 4:
        level = "🟡 Medium"

    else:
        level = "🟢 Strong"

    return level, score, feedback


async def password_strength_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    password = update.message.text

    level, score, feedback = calculate_password_strength(password)

    msg = (
        "🛡 Password Strength Report\n\n"
        f"Strength : {level}\n"
        f"Score : {score}/6\n"
        f"Length : {len(password)}"
    )

    if feedback:
        msg += "\n\nSuggestions:\n"

        for item in feedback:
            msg += f"• {item}\n"

    else:
        msg += "\n\n✅ Excellent password."

    await update.message.reply_text(
        msg,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END
    # ==========================================================
# SHA-256 HASH
# ==========================================================

async def sha256_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    await update.message.reply_text(
        f"🔑 SHA-256 Hash\n\n`{digest}`",
        parse_mode="Markdown",
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
        f"📦 Base64 Encoded\n\n`{encoded}`",
        parse_mode="Markdown",
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# BASE64 DECODE
# ==========================================================

async def base64_decode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    try:

        decoded = base64.b64decode(
            text.encode("utf-8"),
            validate=True
        ).decode("utf-8")

    except UnicodeDecodeError:

        await update.message.reply_text(
            "❌ The Base64 string is valid but does not contain UTF-8 text.",
            reply_markup=back_keyboard(),
        )

        return BASE64_DECODE

    except Exception:

        await update.message.reply_text(
            "❌ Invalid Base64 input.",
            reply_markup=back_keyboard(),
        )

        return BASE64_DECODE

    await update.message.reply_text(
        f"📦 Base64 Decoded\n\n{decoded}",
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END
    # ==========================================================
# UUID GENERATOR
# ==========================================================

async def uuid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = str(uuid.uuid4())

    if update.callback_query:
        await update.callback_query.edit_message_text(
            f"🆔 UUID v4\n\n`{uid}`",
            parse_mode="Markdown",
            reply_markup=back_keyboard(),
        )
    else:
        await update.message.reply_text(
            f"🆔 UUID v4\n\n`{uid}`",
            parse_mode="Markdown",
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END


# ==========================================================
# TIMESTAMP CONVERTER
# ==========================================================

async def timestamp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    try:
        ts = int(text)

        dt = datetime.fromtimestamp(ts)

        result = (
            "⏰ Timestamp Result\n\n"
            f"Unix : {ts}\n"
            f"Date : {dt.strftime('%Y-%m-%d')}\n"
            f"Time : {dt.strftime('%H:%M:%S')}\n"
            f"ISO : {dt.isoformat()}"
        )

    except Exception:

        result = "❌ Invalid Unix Timestamp."

    await update.message.reply_text(
        result,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# UPPERCASE
# ==========================================================

async def uppercase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        update.message.text.upper(),
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# LOWERCASE
# ==========================================================

async def lowercase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        update.message.text.lower(),
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# REVERSE TEXT
# ==========================================================

async def reverse_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text[::-1]

    await update.message.reply_text(
        text,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END


# ==========================================================
# WORD COUNTER
# ==========================================================

async def word_counter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    words = len(text.split())

    chars = len(text)

    chars_no_space = len(text.replace(" ", ""))

    lines = len(text.splitlines())

    result = (
        "📖 Text Statistics\n\n"
        f"Words : {words}\n"
        f"Characters : {chars}\n"
        f"Characters (No Spaces) : {chars_no_space}\n"
        f"Lines : {lines}"
    )

    await update.message.reply_text(
        result,
        reply_markup=back_keyboard(),
    )

    return ConversationHandler.END
    # ==========================================================
# RANDOM TOOLS
# ==========================================================

EMOJIS = [
    "😀","😎","🥳","😂","😍","🤖","🔥","⚡","🎉","💎",
    "🚀","🌟","🍀","🎯","❤️","💯","😇","😈","😺","🦄",
    "🍕","☕","🌈","🎵","📚","💡","🧠","🎁","🏆","🐍"
]

QUOTES = [
    "Believe in yourself.",
    "Stay hungry. Stay foolish.",
    "Never stop learning.",
    "Dream big. Work hard.",
    "Success is earned, not given.",
    "Discipline beats motivation.",
    "One step at a time.",
    "Small progress is still progress.",
    "Great things take time.",
    "Be better than yesterday.",
    "Code. Learn. Repeat.",
    "Focus on solutions.",
    "Consistency creates results.",
    "Everything is figureoutable.",
    "The best time to start is now."
]

# ==========================================================
# RANDOM NUMBER
# ==========================================================

async def random_number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    try:

        minimum, maximum = map(int, text.split())

        if minimum > maximum:
            minimum, maximum = maximum, minimum

        number = random.randint(minimum, maximum)

        await update.message.reply_text(
            f"🎲 Random Number\n\nRange : {minimum} - {maximum}\nResult : **{number}**",
            parse_mode="Markdown",
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

    if update.callback_query:

        await update.callback_query.edit_message_text(
            f"{result}",
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            result,
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END


# ==========================================================
# DICE ROLL
# ==========================================================

async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    value = random.randint(1, 6)

    dice_faces = {
        1: "⚀",
        2: "⚁",
        3: "⚂",
        4: "⚃",
        5: "⚄",
        6: "⚅",
    }

    message = f"🎲 Dice Roll\n\n{dice_faces[value]}\n\nResult : {value}"

    if update.callback_query:

        await update.callback_query.edit_message_text(
            message,
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            message,
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END


# ==========================================================
# RANDOM EMOJI
# ==========================================================

async def random_emoji_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    emoji = random.choice(EMOJIS)

    if update.callback_query:

        await update.callback_query.edit_message_text(
            f"😀 Random Emoji\n\n{emoji}",
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            f"😀 {emoji}",
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END


# ==========================================================
# RANDOM QUOTE
# ==========================================================

async def random_quote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    quote = random.choice(QUOTES)

    if update.callback_query:

        await update.callback_query.edit_message_text(
            f"💬 Quote\n\n_{quote}_",
            parse_mode="Markdown",
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            f"💬 {quote}",
            reply_markup=back_keyboard(),
        )

    return ConversationHandler.END
    # ==========================================================
# GUESS NUMBER GAME
# ==========================================================

GAME_MIN = 1
GAME_MAX = 100
GAME_MAX_ATTEMPTS = 10


async def guess_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    secret = random.randint(GAME_MIN, GAME_MAX)

    guess_numbers[user_id] = {
        "number": secret,
        "attempts": 0,
    }

    message = (
        "🎮 Guess Number Game\n\n"
        f"I'm thinking of a number between {GAME_MIN} and {GAME_MAX}.\n\n"
        "Send your first guess!"
    )

    if update.callback_query:

        await update.callback_query.edit_message_text(
            message,
            reply_markup=back_keyboard(),
        )

    else:

        await update.message.reply_text(
            message,
            reply_markup=back_keyboard(),
        )

    return GUESS_GAME


async def guess_game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in guess_numbers:

        await update.message.reply_text(
            "Start a new game from the menu.",
            reply_markup=back_keyboard(),
        )

        return ConversationHandler.END

    game = guess_numbers[user_id]

    try:

        guess = int(update.message.text)

    except ValueError:

        await update.message.reply_text(
            "❌ Send numbers only.",
            reply_markup=back_keyboard(),
        )

        return GUESS_GAME

    if guess < GAME_MIN or guess > GAME_MAX:

        await update.message.reply_text(
            f"Enter a number between {GAME_MIN} and {GAME_MAX}.",
            reply_markup=back_keyboard(),
        )

        return GUESS_GAME

    game["attempts"] += 1

    target = game["number"]

    if guess == target:

        attempts = game["attempts"]

        del guess_numbers[user_id]

        await update.message.reply_text(
            f"🎉 Correct!\n\n"
            f"Number: {target}\n"
            f"Attempts: {attempts}",
            reply_markup=back_keyboard(),
        )

        return ConversationHandler.END

    remaining = GAME_MAX_ATTEMPTS - game["attempts"]

    if remaining <= 0:

        answer = game["number"]

        del guess_numbers[user_id]

        await update.message.reply_text(
            f"💀 Game Over!\n\n"
            f"The correct number was {answer}.",
            reply_markup=back_keyboard(),
        )

        return ConversationHandler.END

    if guess < target:

        hint = "📉 Too Low"

    else:

        hint = "📈 Too High"

    await update.message.reply_text(
        f"{hint}\n\n"
        f"Attempts: {game['attempts']}/{GAME_MAX_ATTEMPTS}\n"
        f"Remaining: {remaining}\n\n"
        "Try again.",
        reply_markup=back_keyboard(),
    )

    return GUESS_GAME
    # ==========================================================
# CONVERSATION HANDLER
# ==========================================================

conversation_handler = ConversationHandler(

    entry_points=[
        CallbackQueryHandler(callback_router),
    ],

    states={

        FANCY_TEXT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fancy_text_handler,
            )
        ],

        PASSWORD_GEN: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                password_generator_handler,
            )
        ],

        PASSWORD_STRENGTH: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                password_strength_handler,
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

        UUID_GEN: [
            CallbackQueryHandler(
                uuid_handler,
                pattern="^uuid$",
            )
        ],

        TIMESTAMP: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                timestamp_handler,
            )
        ],

        TO_UPPER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                uppercase_handler,
            )
        ],

        TO_LOWER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lowercase_handler,
            )
        ],

        REVERSE_TEXT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                reverse_handler,
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

        COIN_FLIP: [
            CallbackQueryHandler(
                coin_flip_handler,
                pattern="^coin$",
            )
        ],

        DICE: [
            CallbackQueryHandler(
                dice_handler,
                pattern="^dice$",
            )
        ],

        RANDOM_EMOJI: [
            CallbackQueryHandler(
                random_emoji_handler,
                pattern="^emoji$",
            )
        ],

        RANDOM_QUOTE: [
            CallbackQueryHandler(
                random_quote_handler,
                pattern="^quote$",
            )
        ],

        GUESS_GAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                guess_game_handler,
            )
        ],

    },

    fallbacks=[
        CommandHandler(
            "start",
            start,
        ),

        CommandHandler(
            "help",
            help_command,
        ),

        CallbackQueryHandler(
            callback_router,
        ),
    ],

    allow_reentry=True,

)
# ==========================================================
# ERROR HANDLER
# ==========================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception("Exception while handling update:", exc_info=context.error)

    try:

        if isinstance(update, Update):

            target = (
                update.effective_message
                or (
                    update.callback_query.message
                    if update.callback_query
                    else None
                )
            )

            if target:

                await target.reply_text(
                    "⚠️ An unexpected error occurred.\nPlease try again."
                )

    except Exception:
        pass


# ==========================================================
# MAIN
# ==========================================================

def main():

    logger.info("Starting BB877 Utility Bot...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "about",
            about,
        )
    )

    # Conversation
    application.add_handler(conversation_handler)

    # Callback router (fallback for menu buttons)
    application.add_handler(
        CallbackQueryHandler(
            callback_router
        )
    )

    # Error handler
    application.add_error_handler(error_handler)

    logger.info("Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
    
