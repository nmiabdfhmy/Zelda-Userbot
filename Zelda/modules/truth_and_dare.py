import requests

from Zelda import CMD_HANDLER as cmd
from Zelda import CMD_HELP, bot
from Zelda.events import zelda_cmd
from Zelda.utils import edit_or_reply


@bot.on(zelda_cmd(outgoing=True, pattern="truth$"))
async def tede_truth(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/truth").json()
        results = resp["message"]
        await edit_or_reply(event, f"**#Truth**\n\n`{results}`")
    except Exception:
        await edit_or_reply(event, "**Something went wrong LOL...**")


@bot.on(zelda_cmd(outgoing=True, pattern="dare$"))
async def tede_dare(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/dare").json()
        results = resp["message"]
        await edit_or_reply(event, f"**#Dare**\n\n`{results}`")
    except Exception:
        await edit_or_reply(event, "**Something went wrong LOL...**")


CMD_HELP.update(
    {
        "truthdare": f"**Plugin : **`truthdare`\
        \n\n  •  **Syntax :** `{cmd}truth`\
        \n  •  **Function : **Untuk tantangan.\
        \n\n  •  **Syntax :** `{cmd}dare`\
        \n  •  **Function : **Untuk kejujuran.\
    "
    }
)
