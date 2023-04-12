# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Cilik-PyroBot 

from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, upload_file

from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.tools import *

from Cilik.modules.Ubot.help import *

telegraph = Telegraph()
r = telegraph.create_account(short_name="Cilik-Ubot")
auth_url = r["auth_url"]


@Client.on_message(filters.command(["tg", "tgm", "telegraph"], [".", "-", "^","!"]) & filters.me)
async def uptotelegraph(client: Client, message: Message):
    reply = message.reply_to_message
    filesize = 5242880
    Man = await message.reply("💈 `Processing...`")
    # if not replied
    if not reply:
        await Man.edit(
            "**Mohon Balas Ke Pesan, Untuk Mendapatkan Link dari Telegraph.**"
        )
    # replied to text
    elif reply.text:
        if len(reply.text) <= 4096:
            link = telegraph.create_page(
                client.me.first_name,
                html_content=(reply.text.html).replace("\n", "<br>"),
            )
            await Man.edit(
                f"**📌 Uploaded: https://telegra.ph/{link.get('path')}**"
            )
        else:
            await Man.edit("The length text exceeds 4096 characters")
    elif reply.media:
        if (
            reply.photo
            and reply.photo.file_size <= filesize
            or reply.video
            and reply.video.file_size <= filesize
            or reply.animation
            and reply.animation.file_size <= filesize
            or reply.sticker
            and reply.sticker.file_size <= filesize
            or reply.document
            and reply.document.file_size <= filesize
        ):
            if reply.animation or reply.sticker:
                loc = await client.download_media(reply, file_name=f"telegraph.png")
            else:
                loc = await client.download_media(reply)
            try:
                response = upload_file(loc)
            except Exception as e:
                return await Man.edit(f"**ERROR:** `{e}`")
            await Man.edit(
                f"**📌 Uploaded: https://telegra.ph{response[0]}**"
            )
            if os.path.exists(loc):
                os.remove(loc)
        else:
            await Man.edit(
                "Please check the file format or file size , it must be less than 5 mb . . ."
            )
    else:
        await Man.edit("Sorry, The File is not supported !")


