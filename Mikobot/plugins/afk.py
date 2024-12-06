# <============================================== IMPORTS =========================================================>
import html
import random
from datetime import datetime

import humanize
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes, MessageHandler, filters

from Infamous.karma import AFK_IMGS 
from Database.sql import afk_sql as sql
from Mikobot import LOGGER, function
from Mikobot.plugins.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from Mikobot.plugins.users import get_user_id

# <=======================================================================================================>

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


# <================================================ FUNCTION =======================================================>
import random

async def afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text:
        args = update.effective_message.text.split(None, 1)
    else:
        return

    user = update.effective_user

    if not user:  # Ignore channels
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour AFK reason was shortened to 100 characters."
    else:
        reason = ""

    # Set AFK status in the database
    sql.set_afk(user.id, reason)
    fname = user.first_name or "User"

    try:
        # Always include an image
        if reason:
            await update.effective_message.reply_photo(
                photo=random.choice(AFK_IMGS),
                caption=f"⋉ {fname} ɪs ɴᴏᴡ ᴀᴡᴀʏ! \n\n▶︎ Reason: {reason} {notice}",
                parse_mode="Markdown",
            )
        else:
            await update.effective_message.reply_photo(
                photo=random.choice(AFK_IMGS),
                caption=f"⋉ {fname} ɪs ɴᴏᴡ ᴀᴡᴀʏ! {notice}",
                parse_mode="Markdown",
            )
    except BadRequest as e:
        print(f"Error sending AFK message: {e}")


async def no_longer_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    if sql.is_afk(user.id):
        afk_user = sql.check_afk_status(user.id)

        time = humanize.naturaldelta(datetime.now() - afk_user.time)

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "⋉ {} is here!",
                "⋉ {} is back!",
                "⋉ {} is now in the chat!",
                "⋉ {} is awake!",
                "⋉ {} is back online!",
                "⋉ {} is finally here!",
                "⋉ Welcome back! {}",
            ]
            chosen_option = random.choice(options)
            await update.effective_message.reply_text(
                chosen_option.format(firstname)
                + f"\n\nYᴏᴜ ᴡᴇʀᴇ AFK ғᴏʀ: <code>{time}</code>",
                parse_mode="html",
            )
        except:
            return


async def reply_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION],
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION],
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = await get_user_id(
                message.text[ent.offset : ent.offset + ent.length],
            )
            if not user_id:
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = await bot.get_chat(user_id)
            except BadRequest:
                LOGGER.error(
                    "Error: Could not fetch userid {} for AFK module".format(user_id)
                )
                return
            fst_name = chat.first_name

            await check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        await check_afk(update, context, user_id, fst_name, userc_id)


async def check_afk(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    fst_name: str,
    userc_id: int,
):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)

        if int(userc_id) == int(user_id):
            return

        time = humanize.naturaldelta(datetime.now() - user.time)

        if not user.reason:
            res = "⋉ {} ɪs ᴀғᴋ.\n\n▶︎ Lᴀsᴛ sᴇᴇɴ {} ᴀɢᴏ".format(
                fst_name,
                time,
            )
            await update.effective_message.reply_text(res)
        else:
            res = (
                "⋉ {} ɪs ᴀғᴋ.\n\n▶︎ Rᴇᴀsᴏɴ: {}\n▶︎ Lᴀsᴛ sᴇᴇɴ {} ᴀɢᴏ.".format(
                    html.escape(fst_name),
                    html.escape(user.reason),
                    time,
                )
            )
            await update.effective_message.reply_text(res, parse_mode="Markdown")


# <=================================================== HELP ====================================================>


__help__ = """
» /afk <reason>*:* mark yourself as AFK (away from keyboard).

» brb , !afk <reason>*:* same as the afk command - but not a command.

» /bye [Reason > Optional] - Tell others that you are AFK (Away From Keyboard).

» /bye [reply to media] - AFK with media.

» /byedel - Enable auto delete AFK message in group (Only for group admin). Default is **Enable**.

➠ *When marked as AFK, any mentions will be replied to with a message to say you're not available!*
"""

# <================================================ HANDLER =======================================================>
AFK_HANDLER = DisableAbleCommandHandler("afk", afk, block=False)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    filters.Regex(r"^(?i:(brb|!afk))( .*)?$"), afk, friendly="afk", block=False
)
NO_AFK_HANDLER = MessageHandler(
    filters.ALL & filters.ChatType.GROUPS, no_longer_afk, block=False
)
AFK_REPLY_HANDLER = MessageHandler(
    filters.ALL & filters.ChatType.GROUPS, reply_afk, block=False
)

function(AFK_HANDLER, AFK_GROUP)
function(AFK_REGEX_HANDLER, AFK_GROUP)
function(NO_AFK_HANDLER, AFK_GROUP)
function(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "Aғᴋ"
__command_list__ = ["afk"]
__handlers__ = [
    (AFK_HANDLER, AFK_GROUP),
    (AFK_REGEX_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REPLY_GROUP),
]
# <================================================ END =======================================================>
