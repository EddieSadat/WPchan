import discord
from discord.ext import commands
from discord.utils import find
# from datetime import datetime, timezone
from datetime import datetime, timedelta
import pandas as pd
import openai
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)


def wplist(mode = 0):
    df = pd.read_csv('wplist.csv')
    if mode == 0:
        msg = '## Suggested WPs\n'
        for row in range(len(df)):
            if not df.iloc[row].Completed:
                msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
    elif mode == 1:
        msg = '## Completed WPs\n'
        for row in range(len(df)):
            if df.iloc[row].Completed:
                msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
    elif mode == 2:
        msg = '## All WPs\n'
        for row in range(len(df)):
            if not df.iloc[row].Completed:
                msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
            elif df.iloc[row].Completed:
                    msg += f'- ~~[{df.iloc[row].Title}](<{df.iloc[row].Link}>)~~ (Completed)\n'
                    
    return(msg)


def wpentry(title: str, link: str, completed: bool):
    df = pd.read_csv('wplist.csv')
    df.loc[len(df)] = [title, link, completed]
    df.to_csv('wplist.csv', index = False)

    return(f'[{title}](<{link}>)')


def wpdelete(title: str):
    df = pd.read_csv('wplist.csv')
    df.drop(df.loc[df.Title == 'BECK'].index).reset_index(drop=True)
    df.to_csv('wplist.csv', index = False)

    return(title)


def generate_dates_until_count(start_date_str, ep_count):
    current_year = datetime.now().year
    start_date = datetime.strptime(f"{current_year}-{start_date_str}", "%Y-%m-%d")

    dates = []
    count = 1
    i = 0

    while count <= ep_count:
        day = start_date + timedelta(days=i)
        day_name = day.strftime('%a')
        date_str = day.strftime('%m-%d')

        # Weekend logic: Fri, Sat, Sun = +2
        if day_name in ['Fri', 'Sat', 'Sun']:
            increment = 2
        else:
            increment = 1

        if increment == 1:
            label = f"{count}"
        else:
            if count + 1 > ep_count:
                # Don't go beyond target_count
                label = f"{count}"
                increment = 1
            else:
                label = f"{count}-{count + 1}"

        dates.append(f"{day_name}, {date_str}: {label}")
        count += increment
        i += 1

    return dates


@bot.command()
async def list(ctx, mode=0):
    await ctx.reply(wplist(mode))

# @bot.command()
# async def entry(ctx, link, *, title, completed = False):
#     await ctx.reply(f'{title}, {link}, {completed}')
#     await ctx.reply(f"Sucessfully added {wpentry(title, link, completed)}")

@bot.command()
async def entry(ctx, *, args):
    title = args[:args.index(" https:")]
    link = args[args.index(" https:")+1:]
    completed = False
    # await ctx.reply(args + '\n' + args[:args.index(" https:")] + '\n' + args[args.index(" https:")+1:])
    await ctx.reply(f"Sucessfully added {wpentry(title, link, completed)}")

@bot.command()
async def delete(ctx, title):
    await ctx.reply(f'Successfully deleted {wpdelete(title)}')

# @bot.command()
# async def replace(ctx, ):
#     await ctx.reply(f'Successfully replaced {wpdelete(title)}')

# @bot.command()
# async def info(ctx, title):
#     await ctx.reply(f'Successfully deleted {wpdelete(title)}')

@bot.command()
async def schedule(ctx, start_date, episodes: int, *, title):
    dates = generate_dates_until_count(start_date, episodes)
    msg = ""
    for d in dates:
        if d[:3] == 'Sun':
            msg += f'{d}\n------------------\n'
        else:
            msg += f'{d}\n'

    await ctx.reply(f"### {title}\n```\n{msg}```")


# ==== Channel Preference on_guild_join ===============
@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'anime', guild.text_channels)
    target_channel = general if general and general.permissions_for(guild.me).send_messages else guild.text_channels[0]
    embed = discord.Embed(title='WPchan at your service!')
    embed.set_image(url="https://64.media.tumblr.com/tumblr_mb5yq0Rn7u1qdbg24o2_500.gif")
    await target_channel.send(embed=embed)
    # await target_channel.send("https://64.media.tumblr.com/tumblr_mb5yq0Rn7u1qdbg24o2_500.gif")


@bot.event
async def on_guild_remove(guild):
    print("Left guild.")



bot.run(os.getenv("DISCORD_KEY"))