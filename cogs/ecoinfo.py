import discord
from discord.ext import commands
import json
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
    
    
class ecoinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        await open_account(ctx.author)
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          user = ctx.author
      
          users = await get_bank_data(ctx.author)
      
          wallet_amt = users[0]
          bank_amt = users[1]
      
          em = discord.Embed(title=f"{ctx.author.name}'s balance.",description=f"**Wallet:** ₪ {wallet_amt} \n**Bank:** ₪ {bank_amt}",color=discord.Color.teal())
      
          await ctx.send(embed=em)
    
    @commands.command(aliases=['with'])
    async def withdraw(self,ctx,amount:str):
        await open_account(ctx.author)        
        bal = get_bank_data(ctx.author)
        if bal[3] == 1:
           await ctx.send("You are **banned** from this bot!")
        else:
          if amount == None:
              await ctx.send("Please enter the amount!")
              return
      
          bal = await get_bank_data(ctx.author)
          if amount == "all":
              amount = bal[1]
      
          amount = int(amount)
          if amount>=bal[1]:
              await ctx.send("You don't have that much money! lol imagine being broke smh")
              return
          if amount<0:
              await ctx.send("Must be more than 0!")
              return
      
          await update_bank(ctx.author,amount)
          await update_bank(ctx.author,-1*amount,"bank")
      
          await ctx.send(f"You withdrew ₪ {amount} coins!")
      
    @commands.command(aliases=['dep'])
    async def deposit(self,ctx,amount:str):
        await open_account(ctx.author)
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
          if amount>=bal[0]:
              await ctx.send("You don't have that much money! lol imagine being broke smh")
              return
          if amount<0:
              await ctx.send("Must be more than 0!")
              return
      
          await update_bank(ctx.author,-1*amount)
          await update_bank(ctx.author,amount,"bank")
      
          await ctx.send(f"You deposited ₪ {amount} coins!")

def setup(bot):
    bot.add_cog(ecoinfo(bot))
