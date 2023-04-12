# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Cilik-PyroBot

import sys
from os import environ, execle, remove

from pyrogram import Client, filters
from pyrogram.types import Message

from Cilik import BOTLOG_CHATID, LOGGER
from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.misc import HAPP

from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.command("restart", [".", "-", "^", "!", "?"]) & filters.me)
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply("⏳ `Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("✅ **Bot has restarted !**\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Cilik"]
        execle(sys.executable, *args, environ)


@Client.on_message(filters.command(["shutdown", "off"], [".", "-", "^", "!", "?"]) & filters.me)
async def shutdown_bot(client: Client, message: Message):
    if BOTLOG_CHATID:
        await client.send_message(
            BOTLOG_CHATID,
            "**#SHUTDOWN** \n"
            "**Cilik-Userbot** telah di matikan!\nJika ingin menghidupkan kembali silahkan buka heroku",
        )
    await message.reply("🔌 **Cilik-Userbot Berhasil di matikan!**")
    if HAPP is not None:
        HAPP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@Client.on_message(filters.command("logs", [".", "-", "^", "!", "?"]) & filters.me)
async def logs_ubot(client: Client, message: Message):
    if HAPP is None:
        return await edit_or_reply(
            message,
            "Pastikan `HEROKU_API_KEY` dan `HEROKU_APP_NAME` anda dikonfigurasi dengan benar di config vars heroku",
        )
    Man = await message.reply("🧾 `Get Logs your Bots...`")
    with open("Logs-Heroku.txt", "w") as log:
        log.write(HAPP.get_log())
    await client.send_document(
        message.chat.id,
        "Logs-Heroku.txt",
        thumb="Cilik/resources/Cilik.jpg",
        caption="**This is your Heroku Logs**",
    )
    await Man.delete()
    remove("Logs-Heroku.txt")


add_command_help(
    "system",
    [
        [".restart", "Untuk merestart userbot."],
        [".shutdown or off", "Untuk mematikan userbot."],
        [".logs", "Untuk melihat logs userbot."],
    ],
)
