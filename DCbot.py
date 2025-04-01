import discord
import json
import get_data
import asyncio
import get_admission_list
import get_school_list
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "/", intents = intents)

@bot.event
async def on_ready():
    global database
    global adm_list
    global passcount
    global school_list
    try:
        with open('For_Fun/json/database.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        with open('For_Fun/json/passcount.json', 'r', encoding='utf-8') as f:
            passcount = json.load(f)
    except:
        get_data.update()
        with open('For_Fun/json/database.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        with open('For_Fun/json/passcount.json', 'r', encoding='utf-8') as f:
            passcount = json.load(f)
        

    try:
        with open('For_Fun/json/admission.json', 'r', encoding='utf-8') as f:
            adm_list = json.load(f)
    except:
        get_admission_list.get()
        with open('For_Fun/json/admission.json', 'r', encoding='utf-8') as f:
            adm_list = json.load(f)

    try:
        with open('For_Fun/json/school_list.json', 'r', encoding='utf-8') as f:
            school_list = json.load(f)
    except:
        get_school_list.get_school_list()
        with open('For_Fun/json/school_list.json', 'r', encoding='utf-8') as f:
            school_list = json.load(f)

    

    print(f"目前登入身份 --> {bot.user}")
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("查榜機器人已上線 !")
                break

@bot.command()
async def update(ctx):
    await ctx.send("更新資料庫中...這可能需要點時間")
    steps = await asyncio.to_thread(lambda : list(get_data.update()))
    await ctx.send(f"更新完成 ! {steps[4]}")

@bot.command()
async def bye(ctx):
    await ctx.send("感謝使用 !")
    bot.close()

@bot.command()
async def search(ctx, id):
    if id in database:
        embed = discord.Embed(title=f"准考證號碼 {id} 錄取 : ",description="", color=0x58c5e9)
        for i in range(len(database[f'{id}'])):
            embed.add_field(name=f"{database[f'{id}'][i]}", value=f"該科系錄取 {passcount[database[f'{id}'][i]][0]} 人", inline=False)
        await ctx.send(embed=embed)
    elif id in passcount:
        key = ""
        for code, deps in school_list.items():
            if id in deps:
                key = code
                break

        dep_code = ""
        for names, codes in school_list[key].items():
            if id == names:
                dep_code = codes
                break

        embed = discord.Embed(title=f"{id}校系錄取狀況 : ",description="", color=0x58c5e9)
        embed.add_field(name="錄取名單", value=f"[點我打開](https://www.cac.edu.tw/CacLink/apply114/114appLy_3Hd_SieVe_QueRy_9dS4cqa1g_Kp3z/html_sieve_114_Ja9z51F/ColPost/web/common/{dep_code}.htm)", inline=False)

        try:
            info = id.split('-')
            temp = ""
            for data in adm_list[info[0].strip()][info[1].strip()]:
                temp += data
                temp += " / "
            temp.rstrip()
            embed.add_field(name="去年錄取狀況", value=f"{temp}", inline=False)
        except:
            embed.add_field(name="去年錄取狀況", value=f"本校系沒有去年的錄取資料", inline=False)

        
        embed.add_field(name="錄取標準請參考下方網站或圖片下方網站或圖片", value=f"[點我打開](https://www.cac.edu.tw/CacLink/apply114/114appLy_3Hd_SieVe_QueRy_9dS4cqa1g_Kp3z/html_sieve_114_Ja9z51F/Standard/report/{key}.htm)", inline=False)
        embed.set_image(url=f"https://www.cac.edu.tw/CacLink/apply114/114appLy_3Hd_SieVe_QueRy_9dS4cqa1g_Kp3z/html_sieve_114_Ja9z51F/Standard/report/pict/{key}.png") 
        await ctx.send(embed=embed)
        
                
    else:
        await ctx.send("無效的輸入或沒有錄取紀錄 ! ")

bot.run("MTM0MzQyNDc1NDQyNTc5NDY2MA.GV8W1Y.brAQHm66dFaD5URaIuBS-zYLeyGlxwMgJIOX1c")

