# ========================================================== 

# BB877 Utility Bot

# Version 3.0

# Production Build

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

    ConversationHandler,

    MessageHandler,

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

    SHA1_HASH,

    SHA512_HASH,

    MD5_HASH,



    BASE64_ENCODE,

    BASE64_DECODE,



    UUID_GENERATOR,

    TIMESTAMP,



    TEXT_UPPER,

    TEXT_LOWER,

    TEXT_TITLE,

    TEXT_REVERSE,

    WORD_COUNTER,

    CHARACTER_COUNTER,

    REMOVE_SPACES,

    REMOVE_DUPLICATES,



    RANDOM_NUMBER,



    GUESS_NUMBER,



) = range(21)



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

    "😀","😁","😂","🤣","😎","🥳","🤖","🔥","⚡","🎉",

    "🍀","🎯","💎","🚀","❤️","🌈","🐍","🎁","🏆","🍕",

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



    return InlineKeyboardMarkup([

        [

            InlineKeyboardButton(

                "⬅ Back to Home",

                callback_data="home",

            )

        ]

    ])





# ==========================================================

# PASSWORD MENU

# ==========================================================



async def show_password_menu(query):



    await query.edit_message_text(

        text="🔐 *Password Tools*\n\nChoose a tool.",

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





# ==========================================================

# ENCODING MENU

# ==========================================================



async def show_encoding_menu(query):



    await query.edit_message_text(

        text="🔒 *Encoding & Hashing*\n\nChoose a tool.",

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

                    "SHA-1",

                    callback_data="sha1",

                )

            ],



            [

                InlineKeyboardButton(

                    "SHA-512",

                    callback_data="sha512",

                )

            ],



            [

                InlineKeyboardButton(

                    "MD5",

                    callback_data="md5",

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





# ==========================================================

# TEXT MENU

# ==========================================================



async def show_text_menu(query):



    await query.edit_message_text(

        text="📝 *Text Tools*\n\nChoose a tool.",

        parse_mode=ParseMode.MARKDOWN,

        reply_markup=InlineKeyboardMarkup([



            [

                InlineKeyboardButton(

                    "🔠 UPPERCASE",

                    callback_data="upper",

                )

            ],



            [

                InlineKeyboardButton(

                    "🔡 lowercase",

                    callback_data="lower",

                )

            ],



            [

                InlineKeyboardButton(

                    "📝 Title Case",

                    callback_data="title",

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

                    "🔢 Character Counter",

                    callback_data="characters",

                )

            ],



            [

                InlineKeyboardButton(

                    "🧹 Remove Extra Spaces",

                    callback_data="spaces",

                )

            ],



            [

                InlineKeyboardButton(

                    "📄 Remove Duplicate Lines",

                    callback_data="duplicates",

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

# RANDOM MENU

# ==========================================================



async def show_random_menu(query):



    await query.edit_message_text(

        text="🎲 *Random Tools*\n\nChoose a tool.",

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

# START

# ==========================================================



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):



   text = (
    "👋 *Welcome to BB877 Utility Bot*\n\n"

    "A production-grade multi-purpose Telegram Utility Bot.\n\n"

    "*Available Features*\n\n"

    "✨ *Fancy Text*\n"
    "• Stylish Unicode Text Converter\n\n"

    "🔐 *Password Tools*\n"
    "• Password Generator\n"
    "• Password Strength Checker\n\n"

    "🔒 *Encoding & Hashing*\n"
    "• SHA-256\n"
    "• SHA-1\n"
    "• SHA-512\n"
    "• MD5\n"
    "• Base64 Encode\n"
    "• Base64 Decode\n"
    "• UUID Generator\n"
    "• Unix Timestamp Converter\n\n"

    "📝 *Text Tools*\n"
    "• UPPERCASE\n"
    "• lowercase\n"
    "• Title Case\n"
    "• Reverse Text\n"
    "• Word Counter\n"
    "• Character Counter\n"
    "• Remove Extra Spaces\n"
    "• Remove Duplicate Lines\n\n"

    "🎲 *Random Tools*\n"
    "• Random Number\n"
    "• Coin Flip\n"
    "• Dice Roll\n"
    "• Random Emoji\n"
    "• Random Quote\n\n"

    "🎮 *Mini Game*\n"
    "• Guess the Number\n\n"

    "👇 Select a category below."
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

        "*BB877 Utility Bot*\n\n"



        "Available Categories:\n\n"



        "✨ Fancy Text\n"

        "🔐 Password Tools\n"

        "🔒 Encoding & Hashing\n"

        "📝 Text Tools\n"

        "🎲 Random Tools\n"

        "🎮 Guess Number\n\n"



        "Navigate using the buttons below."

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



        "Version: 3.0\n"

        "Framework: python-telegram-bot 21.10\n"

        "Python: 3.12\n"

        "Deployment: Railway\n\n"



        "A multi-purpose Telegram Utility Bot."

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

# CALLBACK ROUTER

# ==========================================================



async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):



    query = update.callback_query

    await query.answer()



    data = query.data



    # ======================================================

    # HOME

    # ======================================================



    if data == "home":

        return await start(update, context)



    # ======================================================

    # HELP / ABOUT

    # ======================================================



    elif data == "help":

        return await help_command(update, context)



    elif data == "about":

        return await about(update, context)



    # ======================================================

    # PASSWORD MENU

    # ======================================================



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

            "🛡 Send a password:",

            reply_markup=back_keyboard(),

        )

        return PASSWORD_STRENGTH



    # ======================================================

    # ENCODING MENU

    # ======================================================



    elif data == "encoding":

        await show_encoding_menu(query)

        return ConversationHandler.END



    elif data == "sha256":

        await query.edit_message_text(

            "🔒 Send text:",

            reply_markup=back_keyboard(),

        )

        return SHA256_HASH



    elif data == "sha1":

        await query.edit_message_text(

            "🔒 Send text:",

            reply_markup=back_keyboard(),

        )

        return SHA1_HASH



    elif data == "sha512":

        await query.edit_message_text(

            "🔒 Send text:",

            reply_markup=back_keyboard(),

        )

        return SHA512_HASH



    elif data == "md5":

        await query.edit_message_text(

            "🔒 Send text:",

            reply_markup=back_keyboard(),

        )

        return MD5_HASH



    elif data == "b64_encode":

        await query.edit_message_text(

            "📦 Send text:",

            reply_markup=back_keyboard(),

        )

        return BASE64_ENCODE



    elif data == "b64_decode":

        await query.edit_message_text(

            "📦 Send Base64 text:",

            reply_markup=back_keyboard(),

        )

        return BASE64_DECODE



    elif data == "uuid":

        return await uuid_handler(update, context)



    elif data == "timestamp":

        await query.edit_message_text(

            "🕒 Send Unix timestamp:",

            reply_markup=back_keyboard(),

        )

        return TIMESTAMP



    # ======================================================

    # TEXT MENU

    # ======================================================



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



    elif data == "title":

        await query.edit_message_text(

            "📝 Send text:",

            reply_markup=back_keyboard(),

        )

        return TEXT_TITLE



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



    elif data == "characters":

        await query.edit_message_text(

            "🔢 Send text:",

            reply_markup=back_keyboard(),

        )

        return CHARACTER_COUNTER



    elif data == "spaces":

        await query.edit_message_text(

            "🧹 Send text:",

            reply_markup=back_keyboard(),

        )

        return REMOVE_SPACES



    elif data == "duplicates":

        await query.edit_message_text(

            "📄 Send text:",

            reply_markup=back_keyboard(),

        )

        return REMOVE_DUPLICATES



    # ======================================================

    # RANDOM MENU

    # ======================================================



    elif data == "random":

        await show_random_menu(query)

        return ConversationHandler.END



    elif data == "random_number":

        await query.edit_message_text(

            "🎲 Send minimum and maximum.\nExample:\n1 100",

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



    # ======================================================

    # GUESS GAME

    # ======================================================



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



    # ======================================================

    # FANCY TEXT

    # ======================================================



    elif data == "fancy":



        await query.edit_message_text(

            "✨ Send text to convert:",

            reply_markup=back_keyboard(),

        )



        return FANCY_TEXT



    # ======================================================

    # UNKNOWN

    # ======================================================



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



    if re.search(

        rf"[{re.escape(PASSWORD_SYMBOLS)}]",

        password,

    ):

        score += 1



    if score <= 1:



        result = "🔴 Very Weak"



    elif score == 2:



        result = "🟠 Weak"



    elif score == 3:



        result = "🟡 Medium"



    elif score == 4:



        result = "🟢 Strong"



    else:



        result = "💪 Very Strong"



    await update.message.reply_text(

        f"🛡 *Password Strength*\n\n{result}",

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

# SHA-1

# ==========================================================



async def sha1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    digest = hashlib.sha1(

        update.message.text.encode("utf-8")

    ).hexdigest()



    await update.message.reply_text(

        f"🔒 *SHA-1*\n\n`{digest}`",

        parse_mode=ParseMode.MARKDOWN,

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# SHA-512

# ==========================================================



async def sha512_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    digest = hashlib.sha512(

        update.message.text.encode("utf-8")

    ).hexdigest()



    await update.message.reply_text(

        f"🔒 *SHA-512*\n\n`{digest}`",

        parse_mode=ParseMode.MARKDOWN,

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# MD5

# ==========================================================



async def md5_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    digest = hashlib.md5(

        update.message.text.encode("utf-8")

    ).hexdigest()



    await update.message.reply_text(

        f"🔒 *MD5*\n\n`{digest}`",

        parse_mode=ParseMode.MARKDOWN,

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# BASE64 ENCODE

# ==========================================================



async def base64_encode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    encoded = base64.b64encode(

        update.message.text.encode("utf-8")

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

# TITLE CASE

# ==========================================================



async def titlecase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    await update.message.reply_text(

        update.message.text.title(),

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# REVERSE TEXT

# ==========================================================



async def reverse_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    await update.message.reply_text(

        update.message.text[::-1],

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

        f"Words: `{words}`\n"

        f"Characters: `{chars}`\n"

        f"Lines: `{lines}`"

    )



    await update.message.reply_text(

        result,

        parse_mode=ParseMode.MARKDOWN,

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# CHARACTER COUNTER

# ==========================================================



async def character_counter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    text = update.message.text



    await update.message.reply_text(

        f"🔢 *Character Count*\n\n`{len(text)}`",

        parse_mode=ParseMode.MARKDOWN,

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# REMOVE EXTRA SPACES

# ==========================================================



async def remove_spaces_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    cleaned = " ".join(update.message.text.split())



    await update.message.reply_text(

        cleaned,

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# REMOVE DUPLICATE LINES

# ==========================================================



async def remove_duplicates_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    lines = update.message.text.splitlines()



    seen = set()

    result = []



    for line in lines:



        if line not in seen:



            seen.add(line)

            result.append(line)



    await update.message.reply_text(

        "\n".join(result),

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END



# ==========================================================

# FANCY TEXT

# ==========================================================



NORMAL = (

    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    "abcdefghijklmnopqrstuvwxyz"

    "0123456789"

)



FONTS = {



    "𝗕𝗼𝗹𝗱":

    (

        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"

        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"

        "0123456789"

    ),



    "𝘐𝘵𝘢𝘭𝘪𝘤":

    (

        "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"

        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"

        "0123456789"

    ),



    "𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘":

    (

        "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"

        "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯"

        "0123456789"

    ),



    "𝙼𝚘𝚗𝚘":

    (

        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"

        "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"

        "0123456789"

    ),



    "𝔻𝕠𝕦𝕓𝕝𝕖":

    (

        "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"

        "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"

        "0123456789"

    ),



    "🅂🄰🄽🅂":

    (

        "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹"

        "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓"

        "0123456789"

    ),



    "🅢🅐🅝🅢 🅑🅞🅛🅓":

    (

        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"

        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"

        "0123456789"

    ),



    "ⓒⓘⓡⓒⓛⓔⓓ":

    (

        "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"

        "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"

        "0123456789"

    ),



    "🄲🅄🅁🅅🄴🄳":

    (

        "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"

        "abcdefghijklmnopqrstuvwxyz"

        "0123456789"

    ),



    "🅂🅀🅄🄰🅁🄴":

    (

        "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"

        "abcdefghijklmnopqrstuvwxyz"

        "0123456789"

    ),



    "𝕱𝖗𝖆𝖐𝖙𝖚𝖗":

    (

        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"

        "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"

        "0123456789"

    ),



    "𝕭𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗":

    (

        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"

        "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"

        "0123456789"

    ),



    "𝒮𝒸𝓇𝒾𝓅𝓉":

    (

        "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"

        "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"

        "0123456789"

    ),



    "𝓑𝓸𝓵𝓭 𝓢𝓬𝓻𝓲𝓹𝓽":

    (

        "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"

        "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"

        "0123456789"

    ),



    "Ｓｔｙｌｅ":

    (

        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"

        "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"

        "０１２３４５６７８９"

    ),



}



# ==========================================================

# FONT CONVERTER

# ==========================================================



def convert_font(text: str, alphabet: str) -> str:



    table = dict(zip(NORMAL, alphabet))



    return "".join(

        table.get(ch, ch)

        for ch in text

    )





# ==========================================================

# FANCY TEXT HANDLER

# ==========================================================



async def fancy_text_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):



    text = update.message.text



    output = []



    for name, alphabet in FONTS.items():



        try:



            converted = convert_font(

                text,

                alphabet,

            )



            output.append(

                f"*{name}*\n`{converted}`"

            )



        except Exception:

            pass



    if not output:



        await update.message.reply_text(

            "❌ Unable to convert text.",

            reply_markup=back_keyboard(),

        )



        return ConversationHandler.END



    message = "\n\n".join(output)



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



        minimum, maximum = map(

            int,

            update.message.text.split()

        )



        if minimum > maximum:

            minimum, maximum = maximum, minimum



        number = random.randint(minimum, maximum)



        await update.message.reply_text(

            f"🎲 Random Number\n\n{number}",

            reply_markup=back_keyboard(),

        )



        return ConversationHandler.END



    except Exception:



        await update.message.reply_text(

            "❌ Example:\n1 100",

            reply_markup=back_keyboard(),

        )



        return RANDOM_NUMBER





# ==========================================================

# COIN FLIP

# ==========================================================



async def coin_flip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    result = random.choice(["🪙 Heads", "🪙 Tails"])



    await update.callback_query.edit_message_text(

        f"{result}",

        reply_markup=back_keyboard(),

    )



    return ConversationHandler.END





# ==========================================================

# DICE

# ==========================================================



async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):



    value = random.randint(1, 6)



    await update.callback_query.edit_message_text(

        f"🎲 Dice Roll\n\n{value}",

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

        f"💬 Random Quote\n\n{quote}",

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

            "❌ Please enter a valid number.",

            reply_markup=back_keyboard(),

        )



        return GUESS_NUMBER



    target = context.user_data["guess_number"]



    context.user_data["attempts"] += 1



    attempts = context.user_data["attempts"]



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

# ERROR HANDLER

# ==========================================================



async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception("Unhandled exception:", exc_info=context.error)



# ==========================================================

# MAIN

# ==========================================================



def main():



    application = (

        Application.builder()

        .token(BOT_TOKEN)

        .build()

    )



    # --------------------------------------------------

    # Global Error Handler

    # --------------------------------------------------



    application.add_error_handler(error_handler)



    # --------------------------------------------------

    # Conversation Handler

    # --------------------------------------------------



    conv_handler = ConversationHandler(



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



            SHA1_HASH: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    sha1_handler,

                )

            ],



            SHA512_HASH: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    sha512_handler,

                )

            ],



            MD5_HASH: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    md5_handler,

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



            TEXT_TITLE: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    titlecase_handler,

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



            CHARACTER_COUNTER: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    character_counter_handler,

                )

            ],



            REMOVE_SPACES: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    remove_spaces_handler,

                )

            ],



            REMOVE_DUPLICATES: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    remove_duplicates_handler,

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



        },



        fallbacks=[



            CommandHandler("start", start),

            CommandHandler("help", help_command),

            CommandHandler("about", about),



        ],



        allow_reentry=True,



    )



    # --------------------------------------------------

    # Command Handlers

    # --------------------------------------------------



    application.add_handler(

        CommandHandler("start", start)

    )



    application.add_handler(

        CommandHandler("help", help_command)

    )



    application.add_handler(

        CommandHandler("about", about)

    )



    # --------------------------------------------------

    # Conversation Handler

    # --------------------------------------------------



    application.add_handler(conv_handler)



    # --------------------------------------------------

    # Start Bot

    # --------------------------------------------------



    logger.info("BB877 Utility Bot started.")



    application.run_polling()



# ==========================================================

# ENTRY POINT

# ==========================================================



if __name__ == "__main__":

    main()
