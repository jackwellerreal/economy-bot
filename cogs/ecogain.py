import discord
from discord.ext import commands
import json
import random
import asyncio
from pymongo import MongoClient

f = open('config.json')
config = json.load(f)

auth_url = config("mongodb-url")

async def open_account(user:discord.Member):
    cluster = MongoClient(auth_url)
    db = cluster[""]

    cursor = db[""]

    try:
        post = {"_id": user.id, "wallet": 1000, "bank": 0, "admin": 0, "banned" : 0} 

        cursor.insert_one(post)

    except:
        pass

async def get_bank_data(user:discord.Member):
    cluster = MongoClient(auth_url)
    db = cluster[""]

    cursor = db[""]

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
    db = cluster[""]

    cursor = db[""]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})
    
    
    
class ecogain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['give','pay'])
    async def share(self,ctx,member:discord.Member,amount:int=None):
        await open_account(ctx.author)
        await open_account(member)    
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          if amount == None:
              await ctx.send("Please enter the amount!")
              return
      
          bal = await get_bank_data(ctx.author)
          if amount == "all":
              amount = bal[0]
      
          amount = int(amount)
          if amount>bal[1]:
              await ctx.send("You don't have that much money! lol imagine being broke smh")
              return
          if amount<0:
              await ctx.send("Must be more than 0!")
              return
      
          await update_bank(ctx.author,-1*amount)
          await update_bank(member,amount)
          await ctx.send(f"You sent ₪ {amount} coins to {member.name}!")

    @commands.command()
    async def beg(self, ctx):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
            await ctx.send("You are **banned** from this bot!")
        else:
            user = ctx.author
      
            bal = await get_bank_data(ctx.author)
      
            earnings = random.randrange(101)
            await update_bank(ctx.author,earnings)
            await ctx.send(f"You got ₪ {earnings} coins!")

    @commands.command()
    async def hunt(self, ctx):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          user = ctx.author
      
          bal = await get_bank_data(ctx.author)
      
          earnings = random.randrange(101)
          
          responses = ['rabbit','boar','deer']
      
          choice = random.choice(responses)
          if choice == 'rabbit':
              await ctx.send(f"You found a rabbit and sold it for ₪ {earnings} coins!")
          if choice == 'deer':
              await ctx.send(f"You found a deer and sold it for ₪ {earnings} coins! ")
          if choice == 'boar':
              await ctx.send(f"You found a boar and sold it for ₪ {earnings} coins!")
          await update_bank(ctx.author,earnings)
    
    @commands.command()
    async def fish(self, ctx):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          user = ctx.author
      
          bal = await get_bank_data(ctx.author)
      
          earnings = random.randrange(101)
      
          responses = ['flopper','nemo','fish']
      
          choice = random.choice(responses)
          if choice == 'flopper':
              await ctx.send(f"You found a flopper and sold it for ₪ {earnings} coins! Wait this isn't fortnite")
          if choice == 'nemo':
              await ctx.send(f"Just keep swimming,  just keep swimming also you sold nemo for ₪ {earnings} coins! What would dory say?")
          if choice == 'fish':
              await ctx.send(f"You caught a fish and sold it for ₪ {earnings} coins!")
          await update_bank(ctx.author,earnings)

    @commands.command()
    async def work(self, ctx):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          user = ctx.author
      
          bal = await get_bank_data(ctx.author)
      
          earnings = random.randrange(256)
      
          responses = ['subway','guide','mod','subway','guide','subway','guide','subway','subway']
      
          choice = random.choice(responses)
          if choice == 'subway':
              await ctx.send(f"You worked at subway and made ₪ {earnings} coins! ||subway is best no cap||")
          if choice == 'guide':
              await ctx.send(f"You worked as a Tour Guide for {ctx.guild.name} and got ₪ {earnings} coins! nice")
          if choice == 'mod':
              await ctx.send(f"you worked as a mod and got nitro worth ₪ {earnings} coins! ||go touch grass smh||")
          await update_bank(ctx.author,earnings)
  
    @commands.command()
    async def search(self, ctx):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          user = ctx.author
      
          bal = await get_bank_data(ctx.author)
      
          earnings = random.randrange(101)
      
          responses = ['area51','hospital','air']
      
          choice = random.choice(responses)
          if choice == 'hospital':
              await ctx.send(f"You searched a hospital and found ₪ {earnings} coins! WTF YOU ROBBED SICK PEOPLE?????")
          if choice == 'area51':
              await ctx.send(f"You searched area 51 and found ₪ {earnings} coins! The FBI is onto you ;)")
          if choice == 'air':
              await ctx.send(f"You searched the air and found ₪ {earnings} coins! WAIT HOW DID YOU SEARCH THE AIR???????????")
          await update_bank(ctx.author,earnings)
      
    @commands.command()
    async def slots(self, ctx,amount:int):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
            bet = amount
        
            if bet == None:
                await ctx.send("Please enter an amount!")
                return
              
            bal = await get_bank_data(ctx.author)
            if bal[0]>0:
                if amount == "all":
                    amount = bal[0]        
            else:
                await ctx.send("Amount must be more than 0!")
                return   
        
            bet = int(amount)
            if bet > bal[0]:
                await ctx.send("You don't have that much money! lol imagine being broke smh")
                return
            if bet < 0:
                await ctx.send("Amount must be more than 0!")
                return
            
            slot1 = random.choice(["put emoji list here"])
            slot2 = random.choice(["put emoji list here"])
            slot3 = random.choice(["put emoji list here"])
        
            slotOutput1 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |` \n`|` 🤓 `|` 🤓 `|` 🤓 `|` \n`|                |` "
            slotOutput2 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |` \n`|` {slot1} `|` 🤓 `|` 🤓 `|` \n`|                |`"
            slotOutput3 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |` \n`|` {slot1} `|` 🤓 `|` {slot3} `|` \n`|                |`"
            slotOutput4 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |` \n`|` {slot1} `|` {slot2} `|` {slot3} `|` \n`|                |`"
            slotOutput5 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |`    and won ₪ {3*bet} coins! :tada: (3x your bet) \n`|` {slot1} `|` {slot2} `|` {slot3} `|` \n`|                |`"
            slotOutput6 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |`    and won ₪ {9*bet} coins! :tada: (9x your bet) \n`|` {slot1} `|` {slot2} `|` {slot3} `|` \n`|                |`"
            slotOutput7 = f"`|                |`    You bet ₪ {bet} coins! \n`|                |`    and lost ₪ {bet} coins! <:MH_trol:963555012238262273>\n`|` {slot1} `|` {slot2} `|` {slot3} `|` \n`|                |`"
        
            message = await ctx.send(content=slotOutput1)
            await asyncio.sleep(1)
            await message.edit(content=slotOutput2)
            await asyncio.sleep(1)
            await message.edit(content=slotOutput3)
            await asyncio.sleep(1)
            await message.edit(content=slotOutput4)
        
            if slot1 == slot2 == slot3:
                await update_bank(ctx.author,amount*9,"wallet")
                await asyncio.sleep(1)
                await message.edit(content=slotOutput6)
                return
        
            if slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
                await update_bank(ctx.author,amount*3,"wallet")
                await asyncio.sleep(1)
                await message.edit(content=slotOutput5)
                return
        
            else:
                await update_bank(ctx.author,amount*-1,"wallet")
                await asyncio.sleep(1)
                await message.edit(content=slotOutput7)
                return

def setup(bot):
    bot.add_cog(ecogain(bot))
