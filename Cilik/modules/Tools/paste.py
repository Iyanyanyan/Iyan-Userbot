# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Cilik-PyroBot

import os
import re
import asyncio
from asyncio import gather
from base64 import b64decode
from io import BytesIO

import aiohttp
import requests

import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message

from Cilik.helpers.basic import edit_or_reply
from Cilik.utils.pastebin import paste

from Cilik.modules.Ubot.help import add_command_help

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def Cilikbin(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link


pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")

@Client.on_message(filters.command("paste", [".", "-", "^", "!", "?"]) & filters.me)
async def patebin(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply To A Message With .paste")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await message.reply("Hanya untuk text dan documents.")
    m = await message.reply("Pasting...")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit_text("Anda hanya dapat paste file yang lebih kecil dari 40KB.")
        if not pattern.search(r.document.mime_type):
            return await m.edit_text("Hanya untuk text dan documents.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    link = await Cilikbin(content)
    try:
        await message.reply_photo(
            photo=link,
            quote=False,
            caption=f"**Paste Link:** [Here]({link})",
        )
        await m.delete()
    except Exception:
        await m.edit_text("Here's your paste")
