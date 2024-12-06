from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
import random
import string
import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant, FloodWait
#from database import *
#from utils import *
#from batch import *
import dns.resolver
from pymongo import MongoClient
from Mikobot import app as bot, BOT_USERNAME
from Mikobot.plugins.helper_funcs.chat_status import dev_plus

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
DB_URI = "mongodb+srv://arnavgupta0078:arnav@cluster3301.ojyvd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(DB_URI)
DATABASE = client["Yuki_File_Share"]

# Define the collection
db = DATABASE["files"]

def get_user_token_and_index(user_id):

    user_data = db.find_one({'user_id': user_id})

    if user_data:
        tokens_with_count = [(key, len(value)) for key, value in user_data.items() if key not in ['_id', 'user_id']]
        return tokens_with_count
    return None



def get_user_data(user_id):
    return db.find_one({'user_id': user_id})

def update_user_data(user_id, token, file_id):
    db.update_one(
        {'user_id': user_id},
        {'$push': {token: file_id}},
        upsert=True
    )

def delete_file(user_id, token, index):
    result = db.update_one(
        {'user_id': user_id, token: {'$exists': True}},
        {'$unset': {f"{token}.{index}": ""}}
    )
    db.update_one(
        {'user_id': user_id, token: {'$exists': True}},
        {'$pull': {token: None}}
    )
    return result.modified_count == 1

def delete_token(user_id, token):
    result = db.update_one(
        {'user_id': user_id},
        {'$unset': {token: ""}}
    )
    return result.modified_count > 0

def get_user_tokens(user_id):
    user_data = db.find_one({'user_id': user_id})
    if user_data:
        return [key for key in user_data if key not in ['_id', 'user_id']]
    return []

def get_file_ids_by_token(token):
    for user_data in db.find():
        if token in user_data:
            user_id = user_data['user_id']
            file_ids = user_data[token]
            return user_id, file_ids
    return None, None


def gen_token(length=10):

    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(length))


@bot.on_message(filters.private & filters.command("addfile"))
async def handle_add_file(_, message):
    user_id = message.from_user.id
    reply = message.reply_to_message
    file = (reply.document or reply.video) if reply and (reply.document or reply.video) else None

    if not file:
        await message.reply("Please reply to a document or video.")
        return

    file_id = file.file_id
    token = message.text.split()[1] if len(message.command) == 2 else gen_token()
    update_user_data(user_id, token, file_id)
    linkx = f'{BOT_USERNAME}.t.me?start={token}'
    link = f'{BOT_USERNAME}.t.me?start={{}}'
    await message.reply(
        f"File added to token: `{token}` \n\nClick to copy \n `{linkx}`\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Click here", url=link.format(token))]]
                        ))
    
@dev_plus
@bot.on_message(filters.private & filters.command(["clearfile", "cfile"]))
async def handle_delete_file(_, message):


    user_id = message.from_user.id

    if len(message.command) != 3:
        await message.reply("Usage: /cfile token index")
        return

    token = message.command[1]
    try:
        index = int(message.command[2]) - 1
    except ValueError:
        await message.reply("Invalid index.")
        return

    if delete_file(user_id, token, index):
        await message.reply(f"File deleted from token: {token}")
    else:
        await message.reply("File does not exist in the specified token.")

@bot.on_message(filters.private & filters.command(['gettokens', 'gettk']))
async def GetTokens(_, message):
     user_id = message.from_user.id
     tokens = get_user_token_and_index(user_id)
     string = f"**🌟 Stored tokens in {message.from_user.mention}**:\n"
     for i, (token, file) in enumerate(tokens):
          string += f"{i+1}, `{token}`: **{file}**\n"
     return await message.reply_text(
           text=string, quote=True
     )

@dev_plus
@bot.on_message(filters.private & filters.command(["cleartoken", "deltoken"]))
async def handle_delete_token(_, message):

    user_id = message.from_user.id

    if len(message.command) != 2:
        await message.reply("Please provide a token to delete.")
        return

    token = message.command[1]
    if delete_token(user_id, token):
        await message.reply("Token deleted.")
    else:
        await message.reply("Token does not exist in the database.")
    
@bot.on_message(filters.private & filters.command(["ctoken","checktoken"]))
async def CheckToken(bot, message):

     if not message.from_user:
         return
     user_id = message.from_user.id
     if not len(message.text.split()) == 2:
           return await message.reply_text("Can you provide me token?\n```Example\n/ctoken token```")
     token = message.text.split()[1]
     if not token in get_user_tokens(user_id):
          return await message.reply("Token Seems like invalid 🤔")
     button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("✨ Click here", url=link.format(token))]])
     return await message.reply_text(
         text="Click the below button to Get the all file's..",
         reply_markup=button
     )

@bot.on_message(filters.text)
async def send_file_by_token(_, message):
    # Check if the message starts with /start followed by a token
    if message.text.startswith("/start "):
        # Extract the token from the message
        token = message.text.split("/start ", 1)[1].strip()
        user_id, file_ids = get_file_ids_by_token(token)

        # Check if the token is valid and if files are associated with it
        if not file_ids:
            return await message.reply("No files found for the given token, or the token is invalid.")

        # Send all files linked to the token
        for file_id in file_ids:
            try:
                await message.reply_document(file_id)
            except Exception as e:
                await message.reply(f"Failed to send file: {str(e)}")
#    else:
#        await message.reply("Invalid format. Please use the /start command followed by a valid token.")

__mod_name__ = "Sᴛᴏʀᴀɢᴇ"

__help__ = """
 **File Store bot**:

➩ /addfile:
to upload a file and get a new token
also you can upload a file to a specific token like `/getlink token` with reply to document or video.

➩ /clearfile:
to remove a specific file from token using the index and token `/cfile token 0`

➩ /cleartoken:
To remove a token from user that means all file in the token removd from db.

➩ /checktoken:
Use it with query `/checktoken token` to get link for share.

➩ /gettokens:
to show your all saved tokens in db.
Example: `@deds3c_bot fs token`
"""