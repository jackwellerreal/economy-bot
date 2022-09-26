import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime
from pymongo import MongoClient

intents = discord.Intents().all()
client = commands.Bot(command_prefix=['eco ','Eco ','eco','Eco'], intents=intents)
client.remove_command('help')

auth_url = "mongodb+srv://whatqm:bPboLtKFJCnUhDYo@minty.scl2p.mongodb.net/?"

async def open_account(user:discord.Member):
    cluster = MongoClient(auth_url)
    db = cluster["minty"]

    cursor = db["minty"]

    try:
        post = {"_id": user.id, "wallet": 1000, "bank": 0, "admin": 0, "banned" : 0} 

        cursor.insert_one(post)

    except:
        pass

async def get_bank_data(user:discord.Member):
    cluster = MongoClient(auth_url)
    db = cluster["minty"]

    cursor = db["minty"]

    user_data = cursor.find({"_id": user.id})

    cols = ["wallet", "bank", "admin", "banned"] 

    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data

async def update_bank(user:discord.Member, amount=0, mode="wallet"):
    cluster = MongoClient(auth_url)
    db = cluster["minty"]

    cursor = db["minty"]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})
    
    
@client.event
async def on_ready():
  time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  print(f"\n\n\nI am alive\n\nTime: {time}\n\n")


@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)

counter = 0
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded cog: {filename[:-3]}')
        counter += 1
print(f'Finished loading [{counter}] cogs')


@client.command()
async def help(ctx, command=None):
    if command == None:
      embed=discord.Embed(title="List Of Commands", description="This is a list of commands that you can use! Run `eco help <command>` for more info!", color=0x2ecc71)
      embed.add_field(name="Gain", value="give, beg, hunt, fish, work, search, slots", inline=False)
      embed.add_field(name="Info", value="balance, deposit, withdraw", inline=False)
      embed.add_field(name="Settings (admin commands)", value="setbank, setwallet, reset, resetall, ban, unban, setadmin", inline=False)
      await ctx.send(embed=embed)
    elif command == "give" or "pay" or "share":
      embed=discord.Embed(title="Give", description="This command can be used to give another member some of your money!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco give <user> <amount>`", inline=False)
      await ctx.send(embed=embed)
    elif command == "beg":
      embed=discord.Embed(title="Beg", description="This command can be used to earn some quick cash!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco beg`", inline=False)
      await ctx.send(embed=embed)
    elif command == "hunt":
      embed=discord.Embed(title="Hunt", description="This command can be used to earn some quick cash!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco hunt`", inline=False)
      await ctx.send(embed=embed)
    elif command == "fish":
      embed=discord.Embed(title="Fish", description="This command can be used to earn some quick cash!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco fish`", inline=False)
      await ctx.send(embed=embed)
    elif command == "work":
      embed=discord.Embed(title="Work", description="This command can be used to earn some quick cash!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco work`", inline=False)
      await ctx.send(embed=embed)
    elif command == "search":
      embed=discord.Embed(title="Search", description="This command can be used to earn some quick cash!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco search`", inline=False)
      await ctx.send(embed=embed)
    elif command == "slots":
      embed=discord.Embed(title="Slots", description="This command can be used to gamble some money with a chance to triple it!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco slots <amount>`", inline=False)
      await ctx.send(embed=embed)
    elif command == "balance" or "bal":
      embed=discord.Embed(title="Balance", description="This command can be used to see how much cash you have!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco balance`", inline=False)
      await ctx.send(embed=embed)
    elif command == "deposit" or "dep":
      embed=discord.Embed(title="Deposit", description="This command can be used to move the cash in your wallet to your bank!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco deposit <amount>`", inline=False)
      await ctx.send(embed=embed)
    elif command == "withdraw" or "with":
      embed=discord.Embed(title="Withdraw", description="This command can be used to move the cash in your bank to your wallet!", color=0x2ecc71)
      embed.add_field(name="Usage", value="`eco withdraw <amount>`", inline=False)
      await ctx.send(embed=embed)
      
    

@client.command()
async def ping(ctx):
  await ctx.send(f"Pong! `{round(client.latency * 1000)}ms`")


async def ch_pr():
    await client.wait_until_ready()
    statuses = ["minty sleep.","youtube","icedragon pls help me with code","eco help"]
    while not client.is_closed():
        status = random.choice(statuses)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        await asyncio.sleep(10)

client.loop.create_task(ch_pr())
client.run('OTg4NzE1MDUyODIxNTE2MzI4.GNIMKE.KhaCwYWB6KNEETP0MudjCG7jFS8cmYeeUIOI2o')
