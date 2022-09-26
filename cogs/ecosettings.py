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
    
    
class ecosettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setbank(self,ctx,member:discord.Member,amount:int=None):
        await open_account(member)
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
           await ctx.send("You cannot run this command!")
        else:
          if amount == None:
              await ctx.send("Please enter the amount!")
              return
          amount = int(amount)
          if amount<0:
              await ctx.send("Must be more than 0!")
              return
      
          await update_bank(member,amount,"bank")
          await ctx.send(f"You set {member.name}'s bank to ₪ {amount} coins!")
  
    @commands.command()
    async def setwallet(self,ctx,member:discord.Member,amount:int=None):
        await open_account(member)
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
           await ctx.send("You cannot run this command!")
        else:
          if amount == None:
              await ctx.send("Please enter the amount!")
              return
          amount = int(amount)
          if amount<0:
              await ctx.send("Must be more than 0!")
              return
      
          await update_bank(member,amount)
          await ctx.send(f"You set {member.name}'s wallet to ₪ {amount} coins!")
        
    @commands.command()
    async def reset(self,ctx,member:discord.Member):
        await open_account(member)
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
           await ctx.send("You cannot run this command!")
        else:
          await update_bank(member,0,"bank")
          await update_bank(member,1000,"wallet")
          await ctx.send(f"You reset {member.name}'s wallet and bank!")
      
    @commands.command()
    async def resetall(self,ctx):
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
           await ctx.send("You cannot run this command!")
        else:
          for member in self.ctx.guild.members:
            await open_account(member)
            await update_bank(member,0,"bank")
            await update_bank(member,1000,"wallet")
          await ctx.send(f"You reset everyones wallet and bank!")

    @commands.command()
    async def ban(self,ctx,member:discord.Member):
        await open_account(member)
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
           await ctx.send("You cannot run this command!")
        else:
          bal = await update_bank(member)
          if bal[3] == 1:
            await ctx.send(f"This user is already banned!") 
          else:
            await update_bank(member,0,"bank")
            await update_bank(member,0,"wallet")
            await update_bank(member,1,"banned")
            await ctx.send(f"You banned {member.name} from using this bot!")   
      
    @commands.command()
    async def unban(self,ctx,member:discord.Member):
        await open_account(member)
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
          await ctx.send("You cannot run this command!")
        else:
          bal = await update_bank(member)
          if bal[3] == 0:
            await ctx.send(f"This user isnt banned!") 
          else:
            await update_bank(member,0,"bank")
            await update_bank(member,1000,"wallet")
            await update_bank(member,0,"banned")
            await ctx.send(f"You unbanned {member.name} from using this bot!") 
            
    @commands.command()
    async def setadmin(self,ctx,member:discord.Member):
        await open_account(member)
        bal = await get_bank_data(ctx.author)
        if bal[2] == 0:
           await ctx.send("You cannot run this command!")
        else:
          bal = await update_bank(member)
          if bal[2] == 1:
            await ctx.send(f"This user is already admin!") 
          else:
            await update_bank(member,1,"admin")
            await ctx.send(f"You set {member.name} as an admin!")
            
def setup(bot):
    bot.add_cog(ecosettings(bot))
