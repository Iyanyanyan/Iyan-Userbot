import asyncio
from prettytable import PrettyTable
from pyrogram import Client, filters, enums
from pyrogram.types import Message

from Cilik import CMD_HELP
from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.utility import split_list

heading = "──「 **{0}** 」──\n"

HELP_LOGO = "https://telegra.ph/file/367355c578c38fb782807.jpg"

@Client.on_message(filters.command("help", [".", "-", "^", "!", "?"]) & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command

    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        all_commands = ""
        all_commands += "Please specify which module you want help for!! \nUsage: `.help [module_name]`\n\n"

        ac = PrettyTable()
        ac.header = False
        ac.title = "𝗖𝗶𝗹𝗶𝗸 𝗠𝗼𝗱𝘂𝗹𝗲𝘀"
        ac.align = "l"

        for x in split_list(sorted(CMD_HELP.keys()), 2):
            ac.add_row([x[0], x[1] if len(x) >= 2 else None])

            
        text = "𝗜𝘆𝗮𝗻 𝗠𝗼𝗱𝘂𝗹𝗲𝘀 \n\n"
        text += "🔮 𝗨𝗯𝗼𝘁: -⋟ `alive` -⋟ `heroku` -⋟ `system` -⋟ `update` \n\n"
        text += "⚙️ 𝗧𝗼𝗼𝗹𝘀: -⋟ `create` -⋟ `converter` -⋟ `gcast` -⋟ `info` -⋟ `invite` -⋟ `locks` -⋟ `profile` -⋟ `parse` -⋟ `paste` -⋟ `purge` -⋟ `sangmata` -⋟ `translate` -⋟ `vctools` \n\n"
        text += "🎈 𝗙𝘂𝗻: -⋟ `asupan` -⋟ `animasi` -⋟ `fakeaction` -⋟ `salam` -⋟ `toxic` \n\n"
        text += "🧰 𝗢𝘁𝗵𝗲𝗿: -⋟ `admins` -⋟ `afk` -⋟ `globals` -⋟ `groups` -⋟ `google` -⋟ `join` -⋟ `logs` -⋟ `misc` -⋟ `nulis` -⋟ `spam` -⋟ `sticker` -⋟ `sosmed` -⋟ `pmpermit` \n\n\n"
        text += "📮 𝗣𝗿𝗲𝗳𝗶𝘅 -⋟ `[. - ^ ! ?]`\n"
        text += "     `.help [module_name]`\n"
        
        await message.reply_photo(
           photo=HELP_LOGO,
           caption=text,
        )     
           
    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = "**❓ Help for Modules**\n\n"
            this_command += heading.format(str(help_arg)).upper()

            for x in commands:
                this_command += f"-⋟ `{str(x)}`\n```{str(commands[x])}```\n\n"

            await message.edit(this_command, parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await message.edit(
                "`Please specify a valid module name.`", parse_mode=enums.ParseMode.MARKDOWN
            )
    


def add_command_help(module_name, commands):

    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict
