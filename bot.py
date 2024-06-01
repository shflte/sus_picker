import os
from dotenv import load_dotenv
import discord
import arrow

load_dotenv()  # Load environment variables from .env file

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='@', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 前來報到')

@bot.command(name='sus_picker')
async def sus_picker(ctx, number_of_impostors: int, *members: discord.Member):
    if number_of_impostors > len(members):
        await ctx.send(f"就只有{len(members)}個人，是要怎麼有{number_of_impostors}個內鬼")
        return

    impostors = random.sample(members, number_of_impostors)

    for impostor in impostors:
        try:
            await impostor.send('內鬼')
        except discord.Forbidden:
            await ctx.send(f'沒辦法私訊{impostor.mention}')

    await ctx.send(f'內鬼可以看私訊了')

bot.run(TOKEN)


bot.run(TOKEN)
