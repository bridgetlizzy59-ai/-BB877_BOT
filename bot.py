import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==========================
# Logging
# ==========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# ==========================
# Bot Token
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not found!")

# ==========================
# Main Menu Keyboard
# ==========================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🔤 Fancy Text", callback_data="fancy"),
            InlineKeyboardButton("📝 Text Tools", callback_data="text_tools"),
        ],
        [
            InlineKeyboardButton("🔐 Security", callback_data="security"),
            InlineKeyboardButton("🎮 Fun", callback_data="fun"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

# ==========================
# START COMMAND
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 *Welcome to BB877 Utility Bot!*\n\n"
        "Your all-in-one Telegram Utility Bot.\n\n"
        "Choose a category below to begin."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

# ==========================
# HELP COMMAND
# ==========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "❓ *Help*\n\n"
        "Use the menu buttons to explore all available tools.\n\n"
        "Available Categories:\n"
        "🔤 Fancy Text\n"
        "📝 Text Tools\n"
        "🔐 Security\n"
        "🎮 Fun\n\n"
        "Need assistance?\n"
        "Simply press any button from the main menu."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )

# ==========================
# ABOUT COMMAND
# ==========================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "*BB877 Utility Bot*\n\n"
        "Fast • Private • Free\n\n"
        "Features include:\n"
        "• Fancy Text\n"
        "• Password Generator\n"
        "• Hash Generator\n"
        "• Base64\n"
        "• UUID\n"
        "• Random Tools\n"
        "• Games\n\n"
        "More tools coming soon."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )

      # ==========================
# CALLBACK MENU HANDLER
# ==========================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ======================
    # Fancy Text
    # ======================

    if data == "fancy":

        keyboard = [
            [
                InlineKeyboardButton("✨ Generate Fancy Text", callback_data="coming_soon")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]
        ]

        await query.edit_message_text(
            text=(
                "🔤 *Fancy Text Generator*\n\n"
                "Send any text after selecting Generate.\n\n"
                "The bot will convert it into multiple fancy font styles."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ======================
    # Text Tools
    # ======================

    elif data == "text_tools":

        keyboard = [

            [
                InlineKeyboardButton("🔠 Uppercase", callback_data="coming_soon"),
                InlineKeyboardButton("🔡 Lowercase", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("🔄 Reverse", callback_data="coming_soon"),
                InlineKeyboardButton("📊 Word Counter", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]

        ]

        await query.edit_message_text(
            text="📝 *Text Tools*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ======================
    # Security
    # ======================

    elif data == "security":

        keyboard = [

            [
                InlineKeyboardButton("🔐 Password", callback_data="coming_soon"),
                InlineKeyboardButton("🔒 Strength", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("#️⃣ SHA256", callback_data="coming_soon"),
                InlineKeyboardButton("📦 Base64", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("🆔 UUID", callback_data="coming_soon"),
                InlineKeyboardButton("⏰ Timestamp", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]

        ]

        await query.edit_message_text(
            text="🔐 *Security Tools*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ======================
    # Fun
    # ======================

    elif data == "fun":

        keyboard = [

            [
                InlineKeyboardButton("🎲 Dice", callback_data="coming_soon"),
                InlineKeyboardButton("🪙 Coin", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("🎲 Random", callback_data="coming_soon"),
                InlineKeyboardButton("😊 Emoji", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("💬 Quote", callback_data="coming_soon"),
                InlineKeyboardButton("🎮 Game", callback_data="coming_soon"),
            ],

            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]

        ]

        await query.edit_message_text(
            text="🎮 *Fun Tools*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ======================
    # About
    # ======================

    elif data == "about":

        keyboard = [

            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]

        ]

        await query.edit_message_text(
            text=(
                "*BB877 Utility Bot*\n\n"
                "⚡ Fast\n"
                "🔒 Private\n"
                "🆓 Free\n\n"
                "An all-in-one Telegram Utility Bot."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ======================
    # Help
    # ======================

    elif data == "help":

        keyboard = [

            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]

        ]

        await query.edit_message_text(
            text=(
                "❓ *Help*\n\n"
                "Use the menu buttons to access each tool.\n\n"
                "More tools will be unlocked in the next update."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ======================
    # Main Menu
    # ======================

    elif data == "main":

        await query.edit_message_text(
            text=(
                "👋 *Welcome Back!*\n\n"
                "Choose a category below."
            ),
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    # ======================
    # Coming Soon
    # ======================

    elif data == "coming_soon":

        keyboard = [

            [
                InlineKeyboardButton("⬅️ Back", callback_data="main")
            ]

        ]

        await query.edit_message_text(
            text=(
                "🚧 This feature will be available in the next section of development."
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
