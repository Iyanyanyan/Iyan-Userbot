# Cilik-PyroBot

import asyncio
import time
from datetime import datetime
import speedtest

from pyrogram import Client, filters
from pyrogram.types import Message

from config import *
from Cilik import CMD_HELP, StartTime
from Cilik.helpers.constants import WWW
from Cilik.helpers.expand import expand_url
from Cilik.helpers.PyroHelpers import SpeedConvert, ReplyCheck
from Cilik.helpers.shorten import shorten_url
from Cilik.utils.tools import get_readable_time
from Cilik.helpers.adminHelpers import DEVS
from Cilik.helpers.basic import edit_or_reply
from .help import add_command_help


# Cilik Variable

@Client.on_message(filters.command(["speed", "speedtest"], [".", "!", "-", "^", "?"]) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await message.edit("⚡️ `Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "📥 `Testing download speed . . .`")
    spd.download()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "📤 `Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )


@Client.on_message(filters.command("dc", [".", "!", "-", "^", "?"]) & filters.me)
async def nearest_dc(client: Client, message: Message):
    dc = await client.send(functions.help.GetNearestDc())
    await message.reply(
        WWW.NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc)
    )


@Client.on_message(filters.command("ping", [".", "!", "-", "^", "?"]) & filters.me)
async def pingme(client: Client, message: Message):
    """Ping the assistant"""
    mulai = time.time()
    grey = await message.reply_text("...")
    akhir = time.time()
    await grey.edit_text(f"**🏓 Pong!**\n`{round((akhir - mulai) * 1000,3)}ms`")


@Client.on_message(filters.command("expand", [".", "!", "-", "^", "?"]) & filters.me)
async def expand(client: Client, message: Message):
    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        expanded = await expand_url(url)
        if expanded:
            await message.reply(
                f"<b>Shortened URL</b>: {url}\n<b>Expanded URL</b>: {expanded}",
                disable_web_page_preview=True,
            )
        else:
            await message.reply("No bro that's not what I do")
    else:
        await message.reply("Nothing to expand")


@Client.on_message(filters.command("shorten", [".", "!", "-", "^", "?"]) & filters.me)
async def shorten(client: Client, message: Message):
    keyword = None

    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
        if len(message.command) > 1:
            keyword = message.command[1]
    elif len(message.command) > 2:
        url = message.command[1]
        keyword = message.command[2]
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        shortened = await shorten_url(url, keyword)
        if shortened == "API ERROR":
            txt = "API URL or API KEY not found! Add YOURLS details to config"
        elif shortened == "INVALID URL":
            txt = f"The provided URL: `{url}` is invalid"
        elif shortened == "KEYWORD/URL Exists":
            txt = "The URL or KEYWORD already exists!"
        else:
            txt = f"<b>Original URL</b>: {url}\n<b>Shortened URL</b>: {shortened}"
            await message.reply(txt, disable_web_page_preview=True)
            return
    else:
        txt = "Please provide a URL to shorten"

    await message.edit(txt)
    await asyncio.sleep(3)
    await message.delete()

 
add_command_help(
    "cilik",
    [
        [".ping", "Ping Bot."],
        [".dc", "Dapatkan Telegram DC Anda."],
        [".cilik or .alive", "Perintah ini untuk memeriksa userbot anda berfungsi atau tidak."],
        [   ".speedtest `or` .speed",
            "Menjalankan tes kecepatan di server yang dihosting oleh bot pengguna ini.."
            "Telegram Speedtest dari server Anda..",
        ],
    ],
)
