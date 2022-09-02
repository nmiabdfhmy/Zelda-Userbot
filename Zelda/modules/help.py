# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from Zelda import CHANNEL
from Zelda import CMD_HANDLER as cmd
from Zelda import CMD_HELP, ICON_HELP, bot
from Zelda.utils import edit_delete, edit_or_reply, zelda_cmd

modules = CMD_HELP

def list_split(mList, n):
    for x in range(0, len(mList), n):
        spliter = mList[x: n+x]

        if len(spliter) < n:
            spliter = spliter + \
                [None for y in range(n-len(spliter))]
        yield spliter

@zelda_cmd(pattern="help(?: |$)(.*)")
async def help(event):
    """For help command"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            await edit_delete(event, f"`{args}` **Bukan Nama Modul yang Valid.**")
    else:
        user = await bot.get_me()
        string = ""

        strings = list(list_split(modules, 35))
        mmk = str(strings)

        kntl = (
            mmk.replace("], [", f"\n\n📌 MODULES :\n")
            .replace("[[", f"📌 MODULES :\n")
            .replace("']]", "")
            .replace("'\n", "\n")
            .replace("',", "")
            .replace("'", "• ")
            .replace("]]", "")
        )
        
        for i in CMD_HELP:
            string += "`" + str(i)
            string += f"`\t\t\t{ICON_HELP}\t\t\t"

        await edit_or_reply(
            event,
            f"**Daftar Perintah Untuk [ZELDA USERBOT](https://github.com/nmiabdfhmy/Zelda-Userbot) :**\n\n"
            f"**Jumlah : ** `{len(modules)}` Modules\n"
            f"**Owner : ** [Lord Zelda](https://t.me/UnrealZlda)\n\n"
            f"{kntl}"
            f"\n\nJoin and Support @{CHANNEL}",
        )
        await event.reply(
            f"\n**Contoh Ketik** `{cmd}help ping` **Untuk Melihat Informasi Module**"
        )
