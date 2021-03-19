import discord
from discord.ext import commands
import os
import json


if not os.path.isfile("blackliste.json"):
    data = {"blackliste": []}
    with open("blackliste.json", "w") as neu:
        json.dump(data, neu)

@client.event
async def on_message(message):
    if not message.author.bot:
        ctx = await client.get_context(message, cls=commands.Context)
        if ctx.command is not None:
            await client.process_commands(message)
        else:
            content = message.content.lower()
            with open('blackliste.json', "r") as file:
                liste = json.load(file)["blackliste"]
            if liste:
                for i in liste:
                    if i in content:
                        await message.delete()
                        await message.channel.send(f'{message.author.mention}!'
                                                   f'ACHTUNG Bitte Achte auf deine Wortwahl das word ist auf der blackliste', delete_after=5)
                        break

@client.command(name="add")
async def add(ctx, *, word: str):
    with open("blackliste.json", "r") as f:
        conf = json.load(f)
    if word.lower() in conf["blackliste"]:
        await ctx.channel.send(f"`{word}` ist bereits in der schwarzen Liste.", delete_after=2)
    else:
        conf["blackliste"].append(word.lower())
        with open("blackliste.json", "w") as f:
            json.dump(conf, f)
        await ctx.channel.send(f"`{word}` wurde der schwarzen Liste hinzugefügt.", delete_after=4)
    await ctx.message.delete()

@client.command(name="remove")
async def remove(ctx, *, word: str):
    with open("blackliste.json", "r") as f:
        conf = json.load(f)
    if word.lower() in conf["blackliste"]:
        conf["blackliste"].remove(word.lower())
        with open("blackliste.json", "w") as file:
            json.dump(conf, file)
        await ctx.channel.send(f"`{word}` wurde erfolgreich von der schwarzen Liste entfernt.", delete_after=2)
    else:
        await ctx.channel.send(f"`{word}` ist nicht in der schwarzen Liste.", delete_after=4)
    await ctx.message.delete()


# Die Blacklist.json file wird automatisch erstellt