import discord
from discord.ext import commands
from discord.ui import Select, Button, View
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
    
    
class ecoshop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self,ctx):
        await open_account(ctx.author)        
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
            await ctx.send("You are **banned** from this bot!")
        else:
            select = Select(options=[discord.SelectOption(label="Giveaways",emoji="🎉"),discord.SelectOption(label="Bot Perks",emoji="🤓"),discord.SelectOption(label="Custom Things",emoji="💳"),discord.SelectOption(label="Other Things",emoji="⛳")])
            giveaways=discord.Embed(title="Shop - Giveaways",color=discord.Color.teal())
            giveaways.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            giveaways.add_field(name="🎲 Longer Claim ─ ₪ 15,000",value="This will give you 12 more hours of claim time!",inline=False)
            giveaways.add_field(name="🎲 Bypass Reqs ─ ₪ 15,000",value="This will let you bypass the requirements for giveaways!",inline=False)
            giveaways.set_footer(text="Use .buy <item> to buy an item!")
            bot=discord.Embed(title="Shop - Bot Perks",color=discord.Color.teal())
            bot.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            bot.add_field(name="⏰ Double Income ─ ₪ 50,000",value="This item doubles the money you get from this bot!",inline=False)
            bot.add_field(name="⏰ Triple Income ─ ₪ 100,000",value="This item triples the money you get from this bot!",inline=False)
            bot.add_field(name="⏰ Quadruple Income ─ ₪ 200,000",value="This item quadruples the money you get from this bot!",inline=False)
            bot.set_footer(text="Use .buy <item> to buy an item!")
            custom=discord.Embed(title="Shop - Custom Things",color=discord.Color.teal())
            custom.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            custom.add_field(name="💸 Custom Role ─ ₪ 150,000",value="This will  make a custom role in this server!",inline=False)
            custom.add_field(name="💸 Custom Command ─ ₪ 150,000",value="This will make a custom command in this bot!",inline=False)
            custom.set_footer(text="Use .buy <item> to buy an item!")
            other=discord.Embed(title="Shop - Other Things",color=discord.Color.teal())
            other.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            other.add_field(name="🎳 Auto-Reaction ─ ₪ 100,000",value="This will make carlbot react to a message with a certain word in it!",inline=False)
            other.add_field(name="🎳 Bitro Classic? ─ ₪ 1,000,000",value="This will give you bitro classic!",inline=False)
            other.set_footer(text="Use .buy <item> to buy an item!")

        async def catagory(interaction):
            if select.values[0] == "Giveaways":
                await interaction.response.edit_message(content=None,embed=giveaways,view=view)
            if select.values[0] == "Bot Perks":
                await interaction.response.edit_message(content=None,embed=bot,view=view)
            if select.values[0] == "Custom Things":
                await interaction.response.edit_message(content=None,embed=custom,view=view)
            if select.values[0] == "Other Things":
                await interaction.response.edit_message(content=None,embed=other,view=view)

        view=View()
        view.add_item(select)
        select.callback = catagory
        await ctx.send("pick", view=view)
        
    @commands.command()
    async def buy(self,ctx,*,item=None):
        await open_account(ctx.author)       
        staff = self.bot.get_channel(991539345355980900) 
        bal = await get_bank_data(ctx.author)
        if bal[3] == 1:
            await ctx.send("You are **banned** from this bot!")
        else:
            if item == None:
                await ctx.send("Please enter the item! *if you dont know what to buy run `eco shop`!*")
                return
            else:
                if item.lower() == "bypass" or "bypass reqs" or "bypass requirements" or "bypassrequirements" or "bypassreqs":
                    if bal[0]>=15000:
                        await update_bank(ctx.author,-1*15000)
                        await ctx.send("You bought bypass requirements")
                        await staff.send(f"{ctx.author.mention} just bought **Bypass Reqs** for ₪ 15,000")
                    elif bal[0]<=15000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "longer" or "longer claim" or "longer claim time" or "longerclaim" or "longerclaimtime":
                    if bal[0]>=15000:
                        await update_bank(ctx.author,-1*15000)
                        await ctx.send("You bought longer claim time")
                        await staff.send(f"{ctx.author.mention} just bought **Longer Claim Time** for ₪ 15,000")
                    elif bal[0]<=15000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "double" or "double income" or "doubleincome":
                    if bal[0]>=50000:
                        await update_bank(ctx.author,-1*50000)
                        await ctx.send("You bought double income")
                        await staff.send(f"{ctx.author.mention} just bought **Double Income** for ₪ 15,000")
                    elif bal[0]<=50000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "triple" or "triple income" or "tripleincome":
                    if bal[0]>=100000:
                        await update_bank(ctx.author,-1*100000)
                        await ctx.send("You bought triple income")
                        await staff.send(f"{ctx.author.mention} just bought **Triple Income** for ₪ 15,000")
                    elif bal[0]<=100000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "quadruple" or "quadruple income" or "quadrupleincome" or "four" or "four income" or "fourincome":
                    if bal[0]>=200000:
                        await update_bank(ctx.author,-1*200000)
                        await ctx.send("You bought quadruple income")
                        await staff.send(f"{ctx.author.mention} just bought **Quadruple Income** for ₪ 15,000")
                    elif bal[0]<=200000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "role" or "custom role" or "customrole":
                    if bal[0]>=150000:
                        await update_bank(ctx.author,-1*150000)
                        await ctx.send("You bought a custom role")
                        await staff.send(f"{ctx.author.mention} just bought **Custom Role** for ₪ 15,000")
                    elif bal[0]<=150000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "command" or "custom command" or "customcommand":
                    if bal[0]>=150000:
                        await update_bank(ctx.author,-1*150000)
                        await ctx.send("You bought a custom command")
                        await staff.send(f"{ctx.author.mention} just bought **Custom Command** for ₪ 15,000")
                    elif bal[0]<=150000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "react" or "reaction" or "auto react" or "auto reaction" or "autoreact" or "autoreaction":
                    if bal[0]>=100000:
                        await update_bank(ctx.author,-1*100000)
                        await ctx.send("You bought an auto-reaction")
                        await staff.send(f"{ctx.author.mention} just bought an **Auto-Reaction** for ₪ 15,000")
                    elif bal[0]<=100000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                elif item.lower() == "bitro" or "bitro classic" or "bitroclassic" or "nitro" or "nitro classic" or "nitroclassic":
                    if bal[0]>=1000000:
                        await update_bank(ctx.author,-1*1000000)
                        await ctx.send("You bought bitro classic")
                        await staff.send(f"{ctx.author.mention} just bought **Bitro Classic** for ₪ 15,000")
                    elif bal[0]<=1000000:
                        await ctx.send("You don't have that much money! lol imagine being broke smh")

                else:
                    await ctx.send("that item doesnt exist.")
            

def setup(bot):
    bot.add_cog(ecoshop(bot))
