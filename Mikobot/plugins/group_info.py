from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message 
from Mikobot import app

EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/Yukii_Onna_Bot?startgroup=true"),
    ],
]

@app.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply("༗ Please provide a group username or chat ID.⌥ Example ➾ `/groupinfo YourGroupUsername` or `/groupinfo -1001234567890`")
        return

    group_identifier = message.command[1]

    try:
        if group_identifier.startswith("-100") and group_identifier[1:].isdigit():
            group_id = int(group_identifier)
            group = await app.get_chat(group_id)
        else:
            group = await app.get_chat(group_identifier)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description
    premium_acc = banned = deleted_acc = bot = 0  # You should replace these variables with actual counts.

    response_text = (
        f"༗ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➾ {group.title}\n\n"
        f"⌥ ɢʀᴏᴜᴘ ɪᴅ ➾ `{group.id}`\n"
        f"⌥ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ➾ {total_members}\n"
        f"⌥ ᴜsᴇʀɴᴀᴍᴇ ➾ @{group.username if group.username else 'N/A'}\n"
        f"⌥ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ➾ \n{group_description or 'N/A'}\n\n"
        f"༗ 🄿🄰🅁🄰🄳🄾🅇"
    )

    await message.reply((response_text))

# Command handler to get group status
@app.on_message(filters.command("status") & filters.group)
def group_status(client, message):
    chat = message.chat  # Chat where the command was sent
    status_text = f"⌥ ɢʀᴏᴜᴘ ɪᴅ ➾ `{chat.id}`\n" \
                  f"⌥ ᴛɪᴛʟᴇ ➾ {chat.title}\n" \
                  f"⌥ ᴛʏᴘᴇ ➾ {chat.type}\n"

    if chat.username:  # Not all groups have a username
        status_text += f"⌥ ᴜsᴇʀɴᴀᴍᴇ ➾ @{chat.username}\n\n"
    else:
        status_text += "Username: None"

    message.reply_text((status_text))

__help__ = """
 ⬤ /groupinfo ➾ ɢᴇᴛ ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
 ⬤ /groupdata ➾ ɢᴇᴛ ɢʀᴏᴜᴘ ᴅᴀᴛᴀ.
"""

__mod_name__ = "Gᴄ-Dᴀᴛᴀ"