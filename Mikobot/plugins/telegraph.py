# <============================================== IMPORTS =========================================================>
import os
from datetime import datetime

from PIL import Image
from pyrogram import filters
from telegraph import Telegraph, exceptions, upload_file

from Mikobot import app
from Mikobot.utils.errors import capture_err

# <=======================================================================================================>


# <================================================ FUNCTION =======================================================>
import os
from datetime import datetime
from PIL import Image
from pyrogram import filters
from catbox import CatboxUploader

uploader = CatboxUploader()
TMP_DOWNLOAD_DIRECTORY = "catbox/"

# Ensure directory exists
os.makedirs(TMP_DOWNLOAD_DIRECTORY, exist_ok=True)

@app.on_message(filters.command(["tgm", "tgt"]) & filters.reply)
async def upload_to_catbox(client, message):
    replied_message = message.reply_to_message

    if not replied_message.media:
        await message.reply_text("Reply to a media message to upload it to Cloud.")
        return

    try:
        # Start timer for download
        start = datetime.now()
        downloaded_file_name = await client.download_media(
            replied_message, TMP_DOWNLOAD_DIRECTORY
        )
        download_time = (datetime.now() - start).total_seconds()

        await message.reply_text(
            f"Downloaded in {download_time:.2f} seconds."
        )

        # Resize if it's a .webp file
        if downloaded_file_name.endswith(".webp"):
            resize_image(downloaded_file_name)

        # Upload to Catbox
        start = datetime.now()
        media_urls = uploader.upload_file(downloaded_file_name)
        upload_time = (datetime.now() - start).total_seconds()

        # Respond with success and link
        await message.reply_text(
            f"Uploaded to [Catbox]({media_urls}) in {download_time + upload_time:.2f} seconds. \n -> `{media_urls}`",
            disable_web_page_preview=False,
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
    finally:
        # Cleanup downloaded files
        if os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)


def resize_image(image_path):
    """Resize .webp images to PNG."""
    try:
        with Image.open(image_path) as im:
            im.save(image_path, "PNG")
    except Exception as e:
        raise RuntimeError(f"Failed to resize image: {str(e)}")



# <=================================================== HELP ====================================================>
__help__ = """ 
➠ *TELEGRAPH*:

» /tgm, /tmg*:* `get telegram link of replied media`
 """

__mod_name__ = "Tᴇʟᴇɢʀᴀᴘʜ"
# <================================================ END =======================================================>
