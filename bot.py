import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random

load_dotenv()  # Load environment variables from .env file

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 前來報到')

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        content = message.content.split()[1:]
        if not content:
            await message.channel.send('usage: `@sus_picker <內鬼數量> <成員1> <成員2> ...`')
            return
        if not content[0].isdigit():
            await message.channel.send('繼續亂打')
            return

        number_of_impostors = int(content[0])
        if number_of_impostors < 1 or number_of_impostors > 5:
            await message.channel.send(f"你想要有{number_of_impostors}個內鬼是不是")
            return
        ctx = await bot.get_context(message)
        try:
            members = [await commands.MemberConverter().convert(ctx, member) for member in content[1:]]
        except commands.BadArgument:
            await message.channel.send('不是 這誰')
            return

        if number_of_impostors > len(members):
            await message.channel.send(f"就只有 {len(members)} 個人 是要怎麼有 {number_of_impostors} 個內鬼")
            return
    
        impostors = random.sample(members, number_of_impostors)

        for impostor in impostors:
            if impostor == bot.user:
                await message.channel.send("哈哈選到我了 屁眼")
                continue
            try:
                await impostor.send('內鬼')
            except discord.Forbidden:
                await message.channel.send(f'沒辦法私訊 {impostor.mention}')

        await message.channel.send(f'內鬼可以看私訊了')
    
    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
