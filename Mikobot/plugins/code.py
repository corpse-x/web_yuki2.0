import requests
from Mikobot import app as Mukesh,BOT_NAME,BOT_USERNAME
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters



@Mukesh.on_message(filters.command(["password"]))
async def passwordgen(bot, message):

    try:

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "Exᴀᴍᴘʟᴇ ➛ /password <length>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/password/{a}') 
            x=response.json()["results"]

            await message.reply_text(f"Hᴇʀᴇ ɪs ʏᴏᴜʀ ᴘᴀssᴡᴏʀᴅ ➛ ` {x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ ➛ {e} ")
@Mukesh.on_message(filters.command(["morseencode"]))
async def morse_en(bot, message):

    try:

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "Exᴀᴍᴘʟᴇ ➛ /morseencode <ǫᴜᴇʀʏ>")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/morse/encode/{a}') 
            x=response.json()["results"]

            await message.reply_text(f"`{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Eʀʀᴏʀ ➛ {e} ")
@Mukesh.on_message(filters.command("morsedecode"))
async def morse_de(bot, message):

    try:

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "Exᴀᴍᴘʟᴇ ➛ /morsedecode <ǫᴜᴇʀʏ>")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/morse/decode/{a}') 
            x=response.json()["results"]

            await message.reply_text(f"`{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Eʀʀᴏʀ ➛ {e} ")
@Mukesh.on_message(filters.command(["encode"]))
async def base_en(bot, message):

    try:

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "Exᴀᴍᴘʟᴇ ➛ /encode <query>")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/base/encode/{a}') 
            x=response.json()["results"]

            await message.reply_text(f"` {x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Eʀʀᴏʀ ➛ {e} ")
@Mukesh.on_message(filters.command(["decode"]))
async def base_de(bot, message):

    try:

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "Exᴀᴍᴘʟᴇ ➛ /decode <ǫᴜᴇʀʏ>")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/base/decode/{a}') 
            x=response.json()["results"]

            await message.reply_text(f" `{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Eʀʀᴏʀ ➛ {e} ")                                

__mod_name__ = "Cᴏᴅᴇ"
__help__ = """
 ❍ /encode* ➛* ᴇɴᴄᴏᴅᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ
 ❍ /decode* ➛* ᴅᴇᴄᴏᴅᴇ ᴘʀᴇᴠɪᴏᴜsʟʏ ᴇᴄʀʏᴘᴛᴇᴅ ᴛᴇxᴛ
 ❍ /morseencode* ➛* ᴍᴏʀsᴇ ᴇɴᴄᴏᴅᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ
 ❍ /morsedecode* ➛* ᴅᴇᴄʀʏᴘᴛs ᴘʀᴇᴠɪᴏᴜsʟʏ ᴇᴄʀʏᴘᴛᴇᴅ ᴛᴇxᴛ
 ❍ /password *➛*  ɢɪᴠᴇ ʟᴇɴɢᴛʜ ᴏғ ᴘᴀssᴡᴏʀᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ
 """