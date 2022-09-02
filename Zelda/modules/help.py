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

def split_list(input_list, n):
    """
    Takes a list and splits it into smaller lists of n elements each.
    :param input_list:
    :param n:
    :return:
    """
    n = max(1, n)
    return [input_list[i : i + n] for i in range(0, len(input_list), n)]

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
        for i in CMD_HELP:
            string += "📌 `" + str(i) + "` "

        await edit_or_reply(
            event,
            f"**Daftar Perintah Untuk [ZELDA USERBOT](https://github.com/nmiabdfhmy/Zelda-Userbot) :**\n\n"
            f"**Jumlah : ** `{len(modules)}` Modules\n"
            f"**Owner : ** [Lord Zelda](https://t.me/UnrealZlda)\n\n"
            f"{string}"
            f"\n\nJoin and Support @{CHANNEL}",
        )
        await event.reply(
            f"\n**Contoh Ketik** `{cmd}help ping` **Untuk Melihat Informasi Module**"
        )
