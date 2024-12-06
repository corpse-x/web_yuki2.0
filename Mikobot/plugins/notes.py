# <============================================== IMPORTS =========================================================>
import time

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from Mikobot import StartTime, function
from Mikobot.__main__ import get_readable_time
from Mikobot.plugins.helper_funcs.chat_status import check_admin

# <=======================================================================================================>


# <================================================ FUNCTION =======================================================>
@check_admin(only_dev=True)
async def ptb_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    start_time = time.time()
    message = await msg.reply_text("Pining")
    end_time = time.time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime))

    await message.edit_text(
        "🏓 <b>PONG</b>\n\n"
        "<b>Time taken:</b> <code>{}</code>\n"
        "<b>Uptime:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode=ParseMode.HTML,
    )

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


def ongoing_handler():
    """Returns the CommandHandler for /ongoing"""
    return CommandHandler('ongoing', ongoing)


# <=======================================================================================================>


# <================================================ HANDLER =======================================================>
function(CommandHandler("ping", ptb_ping, block=False))
# <================================================ END =======================================================>
