import os
import requests
import yt_dlp
from pyrogram import filters
from youtube_search import YoutubeSearch
from Mikobot import SUPPORT_CHAT, BOT_NAME
from Mikobot import app as pbot

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

@pbot.on_message(filters.command(["song", "music"]))
def song(client, message):
    message.delete()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chutiya = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    query = " ".join(message.command[1:])
    print(query)
    m = message.reply("🧪")
    
    # Update ydl_opts to include cookies file and headers
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookies": "cookies.txt",  # Path to the cookies file
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }
    }
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

        duration = results[0]["duration"]
        views = results[0]["views"]

    except Exception as e:
        m.edit("**❍ sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ʏᴏᴜᴛᴜʙᴇ.**")
        print(str(e))
        return

    m.edit("❍ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...\n\n❍ ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        rep = f"**❍ ᴛɪᴛʟᴇ ➛** {title[:25]}\n\n**❍ ᴅᴜʀᴀᴛɪᴏɴ ➛** {duration}\n**❍ ᴠɪᴇᴡs ➛** {views}\n\n**❍ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ ➛** {chutiya}"
        dur = time_to_seconds(duration)
        
        message.reply_audio(
            audio_file,
            caption=rep,
            performer=BOT_NAME,
            thumb=thumb_name,
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit(
            f"**❍ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴇʀʀᴏʀ, ʀᴇᴩᴏʀᴛ ᴛʜɪs ᴀᴛ ➛ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](t.me/{SUPPORT_CHAT})**\n**❍ ᴇʀʀᴏʀ ➛** {e}"
        )
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
__mod_name__ = "Sᴏɴɢ"
__help__ = """
/song ➛ ᴛᴏ  ᴅᴏᴡɴʟᴏᴀᴅ   ᴀɴʏ  sᴏɴɢ 

/music ➛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ  sᴏɴɢ"""
    