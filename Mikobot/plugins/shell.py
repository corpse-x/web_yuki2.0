import subprocess
from telegram.constants import ParseMode

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from Mikobot import LOGGER, dispatcher
from Mikobot.plugins.helper_funcs.chat_status import dev_plus


@dev_plus
def shell(update: Update, context: CallbackContext):
    message = update.effective_message
    cmd = message.text.split(" ", 1)
    if len(cmd) == 1:
        message.reply_text("No command to execute was given.")
        return
    cmd = cmd[1]
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = process.communicate()
    reply = ""
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        reply += f"*ᴘᴀʀᴀᴅᴏx \n stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if stderr:
        reply += f"*ᴘᴀʀᴀᴅᴏx \n stdou*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open("shell_output.txt", "w") as file:
            file.write(reply)
        with open("shell_output.txt", "rb") as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id,
            )
    else:
        message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


SHELL_HANDLER = CommandHandler(["sh"], shell, block=False)
dispatcher.add_handler(SHELL_HANDLER)
__mod_name__ = "Sʜᴇʟʟ"
__command_list__ = ["sh"]
__help__ = """
  Oɴʟʏ ғᴏʀ Devs 

 /sh- shell
"""
__handlers__ = [SHELL_HANDLER]