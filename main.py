import discord
from discord.ext import commands
from discord.utils import find
from datetime import datetime, timedelta
import pandas as pd
import openai
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)


def wplist(mode = 0):
    df = pd.read_csv('wplist.csv')

    if mode == 0:
        embed = discord.Embed(title='Suggested', color=0x674ea7)
        msg = ''
        count = 0
        field_num = 1

        for _, row in df.iterrows():
            if not row.Completed:
                msg += f'- [{row.Title}](<{row.Link}>)\n'
                count += 1

                if count % 10 == 0:
                    embed.add_field(name=f'', value=msg, inline=True)
                    msg = ''
                    field_num += 1

        # Add any leftover entries that didn't complete a full 10
        if msg:
            embed.add_field(name=f'', value=msg, inline=True)

    elif mode == 1:
        embed = discord.Embed(title='Completed', color=0x38761d)

        msg = ''
        count = 0
        field_num = 1

        for _, row in df.iterrows():
            if row.Completed:
                msg += f'- [{row.Title}](<{row.Link}>)\n'
                count += 1

                if count % 10 == 0:
                    embed.add_field(name=f'', value=msg, inline=True)
                    msg = ''
                    field_num += 1

        # Add any leftover entries that didn't complete a full 10
        if msg:
            embed.add_field(name=f'', value=msg, inline=True)
    
    return(embed)


def wpadd(title: str, link: str, completed: bool):
    df = pd.read_csv('wplist.csv')
    df.loc[len(df)] = [title, link, completed]
    df.to_csv('wplist.csv', index = False)

    return(f'[{title}](<{link}>)')


def wpdelete(title: str):
    df = pd.read_csv('wplist.csv')
    link = df[df.Title == title].Link.to_string(index = False)
    df = df.drop(df.loc[df.Title == title].index).reset_index(drop=True)
    df.to_csv('wplist.csv', index = False)

    return(f'[{title}](<{link}>)')


def wpcomplete(title: str):
    df = pd.read_csv('wplist.csv')
    link = df[df.Title == title].Link.to_string(index = False)
    df.loc[df.loc[df.Title == title].index, ['Completed']] = True
    df.to_csv('wplist.csv', index = False)

    return(f'[{title}](<{link}>)')


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
                label = f"{count}"
                increment = 1
            else:
                label = f"{count}-{count + 1}"

        dates.append(f"{day_name}, {date_str}: {label}")
        count += increment
        i += 1

    return dates


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Suggested', style=discord.ButtonStyle.blurple)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=wplist(0))

    @discord.ui.button(label='Completed', style=discord.ButtonStyle.green)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=wplist(1))


@bot.command(description='Interactive menu to view suggested and completed WPs.')
async def menu(ctx):
    view = Menu()
    embed = wplist()
    await ctx.reply(embed=embed, view=view)


@bot.command(description='Shows you list of saved anime.')
async def list(ctx, mode=commands.parameter(description="0 = Suggested, 1 = Completed", default=0)):
    embed = wplist(mode)
    await ctx.reply(embed = embed)


@bot.command(description='Add an anime to WP list.')
async def add(ctx, *, args = commands.parameter(description="!add Title Link")):
    title = args[:args.index(" https:")]
    link = args[args.index(" https:")+1:]
    completed = False
    await ctx.reply(f"Sucessfully added {wpadd(title, link, completed)}")


@bot.command(description='Delete an anime from WP list. Deletes from both Suggested and Completed lists.')
async def delete(ctx, *, title=commands.parameter(description="Enter title exactly as it appears on the list.")):
    await ctx.reply(f'Successfully deleted {wpdelete(title)}')


@bot.command(description='Mark an anime as Completed.')
async def complete(ctx, *, title=commands.parameter(description="Enter title exactly as it appears on the list.")):
    await ctx.reply(f'Congrats on completing {wpcomplete(title)}!')


@bot.command(description='Creates an episode schedule for an anime.')
async def schedule(ctx, start_date=commands.parameter(description="Start date: MM-DD"), episodes: int = commands.parameter(description="Number of episodes"), *, title= commands.parameter(description="Title of schedule")):
    dates = generate_dates_until_count(start_date, episodes)
    msg = ""
    for d in dates:
        if d[:3] == 'Sun':
            msg += f'{d}\n------------------\n'
        else:
            msg += f'{d}\n'

    await ctx.reply(f"### {title}\n```\n{msg}```")


@bot.command(description='RNG an anime to WP from your suggestions list.')
async def roll(ctx):
    df = pd.read_csv('wplist.csv')
    df_plan = df[df['Completed'] == False]

    title_msg = await ctx.reply(content='## There is no such thing as ***coincidence*** in this world...')
    await asyncio.sleep(2)
    await title_msg.edit(content='## There is no such thing as ***coincidence*** in this world...\n## ... there is only ***hitsuzen***.')
    await asyncio.sleep(2)
    reply_msg = await ctx.channel.send(content=f'🔻🔺🔻🔺**{df_plan.sample(1).Title.to_string(index = False)}**🔻🔺🔻🔺')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔺🔻🔺🔻**{df_plan.sample(1).Title.to_string(index = False)}**🔺🔻🔺🔻')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔻🔺🔻🔺**{df_plan.sample(1).Title.to_string(index = False)}**🔻🔺🔻🔺')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔺🔻🔺🔻**{df_plan.sample(1).Title.to_string(index = False)}**🔺🔻🔺🔻')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔻🔺🔻🔺**{df_plan.sample(1).Title.to_string(index = False)}**🔻🔺🔻🔺')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔺🔻🔺🔻**{df_plan.sample(1).Title.to_string(index = False)}**🔺🔻🔺🔻')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔻🔺🔻🔺**{df_plan.sample(1).Title.to_string(index = False)}**🔻🔺🔻🔺')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔺🔻🔺🔻**{df_plan.sample(1).Title.to_string(index = False)}**🔺🔻🔺🔻')
    await asyncio.sleep(.7)
    await reply_msg.edit(content=f'🔻🔺🔻🔺**{df_plan.sample(1).Title.to_string(index = False)}**🔻🔺🔻🔺')
    await asyncio.sleep(.7)

    winner = df_plan.sample(1)
    await reply_msg.edit(content=f'## 🏆 ||{winner.Title.to_string(index = False)}|| 🏆\n||{winner.Link.to_string(index = False)}||')


# ==== Channel Preference on_guild_join ===============
@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'anime', guild.text_channels)
    target_channel = general if general and general.permissions_for(guild.me).send_messages else guild.text_channels[0]
    embed = discord.Embed(title='WPchan at your service!')
    embed.set_image(url="https://64.media.tumblr.com/tumblr_mb5yq0Rn7u1qdbg24o2_500.gif")
    await target_channel.send(embed=embed)


@bot.event
async def on_guild_remove(guild):
    print("Left guild.")



bot.run(os.getenv("DISCORD_KEY"))