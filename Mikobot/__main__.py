# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX

# <============================================== IMPORTS =========================================================>
import asyncio
import contextlib
import importlib
import json
import re
import time
import traceback
from platform import python_version
from random import choice
#from Mikobot.plugins.notes import ongoing_handler

import psutil
import pyrogram
import telegram
import telethon
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import (
    BadRequest,
    ChatMigrated,
    Forbidden,
    NetworkError,
    TelegramError,
    TimedOut,
)
from telegram.ext import (
    ApplicationHandlerStop,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.helpers import escape_markdown

from Infamous.karma import *
from Mikobot import (
    BOT_NAME,
    LOGGER,
    OWNER_ID,
    SUPPORT_CHAT,
    SUPPORT_ID,
    TOKEN,
    StartTime,
    app,
    dispatcher,
    function,
    loop,
    tbot,
)
from Mikobot.plugins import ALL_MODULES
from Mikobot.plugins.helper_funcs.chat_status import is_user_admin
from Mikobot.plugins.helper_funcs.misc import paginate_modules

# <=======================================================================================================>

PYTHON_VERSION = python_version()
PTB_VERSION = telegram.__version__
PYROGRAM_VERSION = pyrogram.__version__
TELETHON_VERSION = telethon.__version__


# <============================================== FUNCTIONS =========================================================>
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Mikobot.plugins." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
async def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    await dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    message = update.effective_message
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                await send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                await send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                await IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            lol = await message.reply_photo(
                photo=str(choice(START_IMG)),
                caption=FIRST_PART_TEXT.format(escape_markdown(first_name)),
                parse_mode=ParseMode.MARKDOWN,
            )
            await asyncio.sleep(0.2)
            guu = await update.effective_message.reply_text("Iɴɪᴛɪᴀʟɪᴢɪɴɢ...")
            await asyncio.sleep(1.0)
            await guu.delete()  # Await this line
            await update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(START_BTN),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False,
            )
    else:
        await message.reply_photo(
            photo=str(choice(START_IMG)),
            reply_markup=InlineKeyboardMarkup(GROUP_START_BTN),
            caption="<b>I ᴀᴍ ᴀʟɪᴠᴇ ʜᴜᴍᴀɴ!</b>\n\n<b>Sɪɴᴄᴇ:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


async def extra_command_handlered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #help buttons
    keyboard = [
        [
            InlineKeyboardButton("Cᴏᴍᴍᴀɴᴅs", callback_data="help_back"),
            InlineKeyboardButton("ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/{SUPPORT_CHAT}" ),
        ],
        [
            InlineKeyboardButton("Aɪ-Tᴏᴏʟs", callback_data="ai_command_handler"),
#            InlineKeyboardButton("ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/{SUPPORT_CHAT}" ),
        ],
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="Miko_back"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Pɪᴄᴋ ᴛʜᴇ ᴏᴘᴛɪᴏɴ ʏᴏᴜ ᴘʀᴇғᴇʀ ᴛᴏ ᴏᴘᴇɴ [‎ ](https://files.catbox.moe/6neeir.png)",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def extra_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "extra_command_handler":
        await query.answer()  # Use 'await' for asynchronous calls
        await query.message.edit_text(
            "<b>Cʜᴏᴏsᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴ </b>[‎ ](https://files.catbox.moe/6neeir.png)",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Cᴏᴍᴍᴀɴᴅs", callback_data="help_back"),
                        InlineKeyboardButton("ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/{SUPPORT_CHAT}" ),
                    ],
                    [
                        InlineKeyboardButton("Aɪ-Tᴏᴏʟs", callback_data="ai_command_handler"
                        ),
#                        InlineKeyboardButton("GENSHIN", callback_data="genshin_command_handler"),
                    ],
                    [
                        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="Miko_back"),
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )


async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Aɪ-Tᴏᴏʟs", callback_data="ai_handler"),
            InlineKeyboardButton("IᴍᴀɢᴇGᴇɴ", callback_data="more_aihandlered"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        " *Hᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴs ғᴏʀ* :",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def ai_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "ai_command_handler":
        await query.answer()
        await query.message.edit_text(
            "*Hᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴs ғᴏʀ*:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Aɪ-Tᴏᴏʟs", callback_data="ai_handler"),
                        InlineKeyboardButton(
                            "IᴍᴀɢᴇGᴇɴ", callback_data="more_aihandlered"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "Bᴀᴄᴋ", callback_data="extra_command_handler"
                        ),
                    ],
                ]
            ),
            parse_mode="Markdown",
        )


async def ai_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "ai_handler":
        await query.answer()
        await query.message.edit_text(
            "[𝗔𝗿𝘁𝗶𝗳𝗶𝗰𝗶𝗮𝗹 𝗜𝗻𝘁𝗲𝗹𝗹𝗶𝗴𝗲𝗻𝘁 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻𝘀]:\n\n"
            "All Commands:\n"
            "➽ /askgpt <write query>: A chatbot using GPT for responding to user queries.\n\n"
            "➽ /palm <write prompt>: Performs a Palm search using a chatbot.\n\n"
            "➽ /upscale <reply to image>: Upscales your image quality.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Nᴇxᴛ", callback_data="more_ai_handler"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "Bᴀᴄᴋ", callback_data="ai_command_handler"
                        ),
                    ],
                ],
            ),
            parse_mode="Markdown",
        )


async def more_ai_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "more_ai_handler":
        await query.answer()
        await query.message.edit_text(
            "*Hᴇʀᴇ's ᴍᴏʀᴇ ɪᴍᴀɢᴇ ɢᴇɴ ʀᴇʟᴀᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅs*:\ɴ\ɴ"
            "Cᴏᴍᴍᴀɴᴅ: /meinamix\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴍᴇɪɴᴀᴍɪx ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /darksushi\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴅᴀʀᴋsᴜsʜɪ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /meinahentai\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴍᴇɪɴᴀʜᴇɴᴛᴀɪ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /darksushimix\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴅᴀʀᴋsᴜsʜɪᴍɪx ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /anylora\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴀɴʏʟᴏʀᴀ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴄᴇᴛsᴜᴍɪx\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴄᴇᴛsᴜᴍɪx ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴀɴʏᴛʜɪɴɢ\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴀɴʏᴛʜɪɴɢ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴀʙsᴏʟᴜᴛᴇ\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴀʙsᴏʟᴜᴛᴇ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴅᴀʀᴋᴠ2\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴅᴀʀᴋᴠ2 ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴄʀᴇᴀᴛɪᴠᴇ\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴄʀᴇᴀᴛɪᴠᴇ ᴍᴏᴅᴇʟ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Bᴀᴄᴋ", callback_data="ai_handler"),
                    ],
                ],
            ),
        )


async def more_aihandlered_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "more_aihandlered":
        await query.answer()
        await query.message.edit_text(
            "*Hᴇʀᴇ's ᴍᴏʀᴇ ɪᴍᴀɢᴇ ɢᴇɴ ʀᴇʟᴀᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅs*:\ɴ\ɴ"
            "Cᴏᴍᴍᴀɴᴅ: /meinamix\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴍᴇɪɴᴀᴍɪx ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /darksushi\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴅᴀʀᴋsᴜsʜɪ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /meinahentai\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴍᴇɪɴᴀʜᴇɴᴛᴀɪ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /darksushimix\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴅᴀʀᴋsᴜsʜɪᴍɪx ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /anylora\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴀɴʏʟᴏʀᴀ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴄᴇᴛsᴜᴍɪx\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴄᴇᴛsᴜᴍɪx ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴀɴʏᴛʜɪɴɢ\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴀɴʏᴛʜɪɴɢ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴀʙsᴏʟᴜᴛᴇ\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴀʙsᴏʟᴜᴛᴇ ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴅᴀʀᴋᴠ2\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴅᴀʀᴋᴠ2 ᴍᴏᴅᴇʟ.\n\n"
            "Cᴏᴍᴍᴀɴᴅ: /ᴄʀᴇᴀᴛɪᴠᴇ\n"
            "  • Dᴇsᴄʀɪᴘᴛɪᴏɴ: Gᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪᴍᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴄʀᴇᴀᴛɪᴠᴇ ᴍᴏᴅᴇʟ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Bᴀᴄᴋ", callback_data="ai_command_handler"
                        ),
                    ],
                ],
            ),
        )


async def anime_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "anime_command_handler":
        await query.answer()
        await query.message.edit_text(
            "⛩𝗔𝗻𝗶𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 :\n\n"
            "**╔ /anime: **fetches info on single anime (includes buttons to look up for prequels and sequels)\n"
            "**╠ /character: **fetches info on multiple possible characters related to query\n"
            "**╠ /manga: **fetches info on multiple possible mangas related to query\n"
            "**╠ /airing: **fetches info on airing data for anime\n"
            "**╠ /studio: **fetches info on multiple possible studios related to query\n"
            "**╠ /schedule: **fetches scheduled animes\n"
            "**╠ /browse: **get popular, trending or upcoming animes\n"
            "**╠ /top: **to retrieve top animes for a genre or tag\n"
            "**╠ /watch: **fetches watch order for anime series\n"
            "**╠ /fillers: **to get a list of anime fillers\n"
            "**╠ /gettags: **get a list of available tags\n"
            "**╠ /animequotes: **get random anime quotes\n"
            "**╚ /getgenres: **Get list of available Genres\n\n"
            "**⚙️ Group Settings:**\n"
            "**╔**\n"
            "**╠ /anisettings: **to toggle NSFW lock and airing notifications and other settings in groups (anime news)\n"
            "**╚**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("More Info", url="https://anilist.co/"),
                        InlineKeyboardButton(
                            "Sᴜᴘᴘᴏʀᴛ GC", url="https://t.me/yukilogs"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "Bᴀᴄᴋ", callback_data="extra_command_handler"
                        ),
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )


async def genshin_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "genshin_command_handler":
        await query.answer()
        await query.message.edit_text(
            "⛩ [𝗚𝗲𝗻𝘀𝗵𝗶𝗻 𝗜𝗺𝗽𝗮𝗰𝘁](https://telegra.ph/file/cd03348a4a357624e70db.jpg) ⛩\n\n"
            "*UNDER DEVELOPMENT*",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "More Info", url="https://genshin.mihoyo.com/"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "» 𝘽𝘼𝘾𝙆 «", callback_data="extra_command_handler"
                        ),
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    await context.bot.send_message(
        chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML
    )


# for test purposes
async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    try:
        raise error
    except Forbidden:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "❆ *Hᴇʟᴘ Sᴇᴄᴛɪᴏɴ ᴏғ* *{}* :\n".format(HELPABLE[module].__mod_name__)
                + HELPABLE[module].__help__
            )
            await query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            await query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        await context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass


async def stats_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "insider_":
        uptime = get_readable_time((time.time() - StartTime))
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        text = f"""
Sʏsᴛᴇᴍ Sᴛᴀᴛs Yᴜᴋɪ Oɴɴᴀ 2.0
━━━━━━━━━━━━━━━━━━━
Uᴘᴛɪᴍᴇ ⋉ {uptime}
Cᴘᴜ ⋉ {cpu}%
Rᴀᴍ ⋉ {mem}%
Dɪsᴋ ⋉ {disk}%
━━━━━━━━━━━━━━━━━━━
Pʏᴛʜᴏɴ ⋉ {PYTHON_VERSION}
Pᴛʙ ⋉ {PTB_VERSION}
Tᴇʟᴇᴛʜᴏɴ ⋉ {TELETHON_VERSION}
Pʏʀᴏɢʀᴀᴍ ⋉ {PYROGRAM_VERSION}
━━━━━━━━━━━━━━━━━━━
Bᴏᴛ Vᴇʀsɪᴏɴ ⋉ 2.0-snowhite
"""
        await query.answer(text=text, show_alert=True)


async def gitsource_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "git_source":
        source_link = "https://google.com"
        message_text = (
            f"*Here is the link for the public source repo*:\n\n{source_link}"
        )

        # Adding the inline button
        keyboard = [[InlineKeyboardButton(text="◁", callback_data="Miko_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False,
            reply_markup=reply_markup,
        )


async def repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    source_link = "https://google.com"
    message_text = f"*Here is the link for the public source repo*:\n\n{source_link}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False,
    )


async def Miko_about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "Miko_":
        uptime = get_readable_time((time.time() - StartTime))
        message_text = (
            f"❆ <b>AI-Dʀɪᴠᴇɴ Pᴏᴡᴇʀ</b>"
            f"\n❆ <b>Nᴇxᴛ-Lᴇᴠᴇʟ Aɴɪᴍᴇ Tʜᴇᴍᴇᴅ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ</b>"
            f"\n\n<b>Hɪᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴜɴʟᴏᴄᴋ ᴛʜᴇ ғᴜʟʟ ᴘᴏᴛᴇɴᴛɪᴀʟ ᴏғ {BOT_NAME}!</b>"

        )
        await query.message.edit_text(
            text=message_text,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
#                        InlineKeyboardButton(
#                            text="Aʙᴏᴜᴛ", callback_data="Miko_support"
#                        ),
                        InlineKeyboardButton(text="Cᴏᴍᴍᴀɴᴅs", callback_data="help_back"),
                        InlineKeyboardButton(text="Sᴛᴀᴛs", callback_data="insider_"),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="Miko_back"),
                    ],
                ]
            ),
        )
    elif query.data == "Miko_support":
        message_text = (
            "*Our bot leverages SQL, MongoDB, Telegram, MTProto for secure and efficient operations. It resides on a high-speed server, integrates numerous APIs, ensuring quick and versatile responses to user queries.*"
            f"\n\n*If you find any bug in {BOT_NAME} Please report it at the support chat.*"
        )
        await query.message.edit_text(
            text=message_text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Sᴜᴘᴘᴏʀᴛ ", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="Dᴇᴠ-Sᴀᴍᴀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="Miko_"),
                    ],
                ]
            ),
        )
    elif query.data == "Miko_back":
        first_name = update.effective_user.first_name
        await query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(START_BTN),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            await update.effective_message.reply_text(
                f"Cᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ PM ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏғ {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Hᴇʟᴘ",
                                url="https://t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        await update.effective_message.reply_text(
            "» *Pɪᴄᴋ ᴀɴ ᴏᴘᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ɪᴛ ᴛᴏ ᴋɴᴏᴡ* [‎ ](https://files.catbox.moe/sthpiw.jpg)",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Oᴘᴇɴ ɪɴ Dᴍ",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Sʜᴏᴡ Hᴇʀᴇ",
                            callback_data="extra_command_handler",
                        )
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Hᴇʀᴇ ɪs ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ *{}* ᴍᴏᴅᴜʟᴇ:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        await send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="help_back")]] #back button
            ),
        )

    else:
        await send_help(chat.id, HELP_STRINGS)


async def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            await dispatcher.bot.send_message(
                user_id,
                "Tʜᴇsᴇ ᴀʀᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            await dispatcher.bot.send_message(
                user_id,
                "Sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴜsᴇʀ sᴘᴇᴄɪғɪᴄ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(",
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            await dispatcher.bot.send_message(
                user_id,
                text="Wʜɪᴄʜ ᴍᴏᴅᴜʟᴇ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ {}'s sᴇᴛᴛɪɴɢs ғᴏʀ?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            await dispatcher.bot.send_message(
                user_id,
                "Sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴄʜᴀᴛ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(\nSᴇɴᴅ ᴛʜɪs "
                "Iɴ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ɪɴ ᴛᴏ ғɪɴᴅ ɪᴛ's ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs!",
                parse_mode=ParseMode.MARKDOWN,
            )


async def settings_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* ʜᴀs ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴇᴛᴛɪɴɢs ғᴏʀ ᴛʜᴇ *{}* ᴍᴏᴅᴜʟᴇ:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            await query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁", #back button
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                "Sᴜᴘ ʜᴜᴍᴀɴ! Tʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ"
                "UᴡU sᴏ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ :".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                "Sᴜᴘ ʜᴜᴍᴀɴ! Tʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ"
                "UᴡU sᴏ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ :".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                text="Sᴜᴘ ʜᴜᴍᴀɴ! Tʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ"
                "UᴡU sᴏ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ :".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        await query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


async def get_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Cʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ's sᴇᴛᴛɪɴɢs, ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs ʜᴜᴍᴀɴ"
            await msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Sᴇᴛᴛɪɴɢs",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Sᴜᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs"

    else:
        await send_settings(chat.id, user.id, True)


async def migrate_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, ᴛᴏ %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        with contextlib.suppress(KeyError, AttributeError):
            mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully Migrated!")
    raise ApplicationHandlerStop

# <================================================ ONGOING =======================================================>
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from aiohttp import ClientSession
import json as jloads

async def ongoing(update: Update, context: CallbackContext):
    try:
        # Fetch anime schedule
        async with ClientSession() as ses:
            res = await ses.get("https://subsplease.org/api/?f=schedule&h=true&tz=Asia/Kolkata")
            aniContent = jloads(await res.text())["schedule"]
        
        # Construct the message text
        text = "<b>📆 Today's Anime Releases Schedule [IST]</b>\n\n"
        for i in aniContent:
            aname = i["title"]  # You can modify this to handle more details if necessary
            text += f'''<a href="https://subsplease.org/shows/{i['page']}">{aname}</a>\n    • <b>Time</b> : {i["time"]} hrs\n\n'''

        # Send the formatted message to the user
        await update.message.reply_text(text, parse_mode='HTML', disable_web_page_preview=False)

    except Exception as err:
        # Handle errors and notify the user
        await update.message.reply_text(f"An error occurred while fetching the anime schedule: {err}")
        raise  # Re-raise the exception for logging in the application error handler

def ongoing_handler():
    """Returns the CommandHandler for /ongoing"""
    return CommandHandler('ongoing', ongoing)


# <=======================================================================================================>

# <=======================================================================================================>

# <=================================================== MAIN ====================================================>
def main():
    function(CommandHandler("start", start))
    function(CommandHandler("ongoing", ongoing_handler))

    function(CommandHandler("help", extra_command_handlered))
    function(CallbackQueryHandler(help_button, pattern=r"help_.*"))

    function(CommandHandler("settings", get_settings))
    function(CallbackQueryHandler(settings_button, pattern=r"stngs_"))
#    function(CommandHandler("repo", repo))

    function(CallbackQueryHandler(Miko_about_callback, pattern=r"Miko_"))
    function(CallbackQueryHandler(gitsource_callback, pattern=r"git_source"))
    function(CallbackQueryHandler(stats_back, pattern=r"insider_"))
    function(MessageHandler(filters.StatusUpdate.MIGRATE, migrate_chats))
    function(CallbackQueryHandler(ai_handler_callback, pattern=r"ai_handler"))
    function(CallbackQueryHandler(more_ai_handler_callback, pattern=r"more_ai_handler"))
    function(CallbackQueryHandler(ai_command_callback, pattern="ai_command_handler"))
    function(
        CallbackQueryHandler(anime_command_callback, pattern="anime_command_handler")
    )
    function(
        CallbackQueryHandler(more_aihandlered_callback, pattern="more_aihandlered")
    )
    function(
        CallbackQueryHandler(extra_command_callback, pattern="extra_command_handler")
    )

    function(CommandHandler("ai", ai_command))
    function(
        CallbackQueryHandler(
            genshin_command_callback, pattern="genshin_command_handler"
        )
    )

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("[Yuki 2.0] Starting bot - Using long polling.")
    dispatcher.run_polling(timeout=15, drop_pending_updates=True)
#    await main()

if __name__ == "__main__":
    try:
        LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
        tbot.start(bot_token=TOKEN)
        app.start()
        main()
#        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
    except Exception:
        err = traceback.format_exc()
        LOGGER.info(err)
    finally:
        try:
            if loop.is_running():
                loop.stop()
        finally:
            loop.close()
        LOGGER.info(
            "------------------------ Stopped Services ------------------------"
        )
# <==================================================== END ===================================================>
