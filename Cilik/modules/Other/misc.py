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

import asyncio
import random
from asyncio import sleep
from datetime import datetime

from pyrogram import Client, enums,  filters, raw
from pyrogram.types import Message

from Cilik import *
from Cilik.helpers.basic import edit_or_reply

from Cilik.utils import s_paste
from Cilik.helpers.PyroHelpers import ReplyCheck
from Cilik.helpers.tools import get_arg

from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.command("limit", [".", "-", "^", "!", "?"]) & filters.me)
async def spamban(client: Client, m: Message):
    await client.unblock_user("SpamBot")
    response = await client.send(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    wait_msg = await m.reply("💈 `Processing...`")
    await asyncio.sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await wait_msg.edit_text(f"-⋟ {status.text}")
    
    
@Client.on_message(filters.command(["webshot", "ss"], [".", "-", "^", "!", "?"]) & filters.me)
async def webshot(client: Client, message: Message):
    Man = await message.reply("💈 `Processing...`")
    try:
        user_link = message.command[1]
        try:
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**Screenshot of the page ⟶** {user_link}",
            )
        except Exception as dontload:
            await message.edit(f"Error! {dontload}\nTrying again create screenshot...")
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**Screenshot of the page ⟶** {user_link}",
            )
        await Man.delete()
    except Exception as error:
        await Man.delete()
        await client.send_message(
            message.chat.id, f"**Something went wrong\nLog:{error}...**"
        )

    
@Client.on_message(filters.me & filters.command(["q", "quotly"], [".", "-", "^", "!", "?"]))
async def quotly(client: Client, message: Message):
    args = get_arg(message)
    if not message.reply_to_message and not args:
        return await message.edit("**Mohon Balas ke Pesan**")
    bot = "QuotLyBot"
    if message.reply_to_message:
        await message.edit("`Making a Quote . . .`")
        await client.unblock_user(bot)
        if args:
            await client.send_message(bot, f"/qcolor {args}")
            await asyncio.sleep(1)
        else:
            pass
        await message.reply_to_message.forward(bot)
        await asyncio.sleep(5)
        async for quotly in client.search_messages(bot, limit=1):
            if quotly:
                await message.delete()
                await message.reply_sticker(
                    sticker=quotly.sticker.file_id,
                    reply_to_message_id=message.reply_to_message.id
                    if message.reply_to_message
                    else None,
                )
            else:
                return await message.edit("**Gagal Membuat Sticker Quotly**")


@Client.on_message(filters.command("stats", [".", "-", "^", "!", "?"]) & filters.me)
async def stats(client: Client, message: Message):
    yanto = await message.reply_text("📊 `Collecting stats`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await yanto.edit_text(
        """📊 **Stats Me**
**Private Chats :** `{}`
**Groups:** `{}`
**Super Groups:** `{}`
**Channels:** `{}`
**Admins:** `{}`
**Bots:** `{}`
**⏱ It Took:** `{}`""".format(
            u, g, sg, c, a_chat, b, ms
        )
    )


@Client.on_message(filters.command(["tt", "tiktok", "ig", "sosmed"], [".", "-", "^", "!", "?"]) & filters.me)
async def sosmed(client: Client, message: Message):
    Man = await message.reply("`📥 Downloading...`")
    link = get_arg(message)
    bot = "thisvidbot"
    if link:
        try:
            xnxx = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xnxx.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xnxx.delete()
    async for sosmed in client.search_messages(
        bot, filter=enums.MessagesFilter.VIDEO, limit=1
    ):
        await asyncio.gather(
            Man.delete(),
            client.send_video(
                message.chat.id,
                sosmed,
                caption=f"**Upload by:** {client.me.mention}",
                reply_to_message_id=ReplyCheck(message),
            ),
        )
        await client.delete_messages(bot, 2)
        
        
add_command_help(
    "misc",
    [
        [
            ".q or .quote",
            "To Make a Quote",
        ],
        [".q <warna> atau .quotly <warna>", "Membuat pesan menjadi sticker dengan custom warna background yang diberikan."],
        [".limit", "Check Limit telegram from @SpamBot."],
        [".webshot <link> `atau` .ss <link>", "Untuk Mengscreenshot halaman web yang diberikan."],
        [".stats", "To Check Your Account Status, how Joined Chats."],
        [".tgm", "Reply to Media as args to upload it to telegraph."],
        [".clone", "To Clone someone Profile."],
        [".revert", "To Get Your Account Back."],
        [".carbon", "Carbonised Text."],
    ],
)


add_command_help(
    "sosmed",
    [
        [
            f"sosmed <link>",
            "Untuk Mendownload Media Dari Facebook / Tiktok / Instagram / Twitter / YouTube.",
        ],
    ],
)

