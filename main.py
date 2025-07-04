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


# def wplist(mode = 0):
#     df = pd.read_csv('wplist.csv')

#     if mode == 0:                  
#         # msg = '## Suggested WPs\n'
#         embed=discord.Embed(title = f'Suggested WPs',
#                             color = 0xD0881F)
#         for row in range(len(df)):
#             if not df.iloc[row].Completed:
#                 # msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
#                 embed.add_field(name = '', value = f'[{df.iloc[row].Title}](<{df.iloc[row].Link}>)   ')

#     elif mode == 1:
#         # msg = '## Completed WPs\n'
#         embed=discord.Embed(title = f'Completed WPs',
#                             color = 0xD0881F)
#         for row in range(len(df)):
#             if df.iloc[row].Completed:
#                 # msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
#                 embed.add_field(name = '', value = f'[{df.iloc[row].Title}](<{df.iloc[row].Link}>)   ')

#     elif mode == 2:
#         # msg = '## All WPs\n'
#         embed=discord.Embed(title = f'All WPs',
#                             color = 0xD0881F)
#         for row in range(len(df)):
#             if not df.iloc[row].Completed:
#                 # msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
#                 embed.add_field(name = '', value = f'[{df.iloc[row].Title}](<{df.iloc[row].Link}>)   ')

#             elif df.iloc[row].Completed:
#                 # msg += f'- ~~[{df.iloc[row].Title}](<{df.iloc[row].Link}>)~~ (Completed)\n'
#                 embed.add_field(name = '', value = f'~~[{df.iloc[row].Title}](<{df.iloc[row].Link}>)~~ (Completed)   ')

#     if len(df)%3 == 1:
#         embed.add_field(name = '', value = '')
#     elif len(df)%3 == 2:
#         embed.add_field(name = '', value = '')
#         embed.add_field(name = '', value = '')
                    
#     return(embed)


def wplist(mode = 0):
    df = pd.read_csv('wplist.csv')

    if mode == 0:
        embed = discord.Embed(title='Suggested', color=0x3d85c6)

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

    
        # embed=discord.Embed(title = 'Suggested', color = 0x3d85c6)
        # msg = ''
        # for row in range(len(df)):
        #     if not df.iloc[row].Completed:
        #         msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
        
        # embed.add_field(name='Test', value=msg)
        #         # embed.add_field(name = '', value = f'[{df.iloc[row].Title}](<{df.iloc[row].Link}>)')

    elif mode == 1:
        embed = discord.Embed(title='Suggested', color=0x38761d)

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

        # embed=discord.Embed(title = 'Completed', color = 0x38761d)
        # for row in range(len(df)):
        #     if df.iloc[row].Completed:
        #         # msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
        #         embed.add_field(name = '', value = f'[{df.iloc[row].Title}](<{df.iloc[row].Link}>)')
    
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

    # @discord.ui.button(label='Home', style=discord.ButtonStyle.gray)
    # async def list(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     embed = wplist()
    #     await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='Suggested', style=discord.ButtonStyle.blurple)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        # embed = discord.Embed(color=discord.Color.random())
        # embed.set_author(name='This is an edited embed')
        # embed.add_field(name='YO', value='FUN')
        await interaction.response.edit_message(embed=wplist(0))

    @discord.ui.button(label='Completed', style=discord.ButtonStyle.green)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        # embed = discord.Embed(color=discord.Color.random())
        # embed.set_author(name='This is an edited embed')
        # embed.add_field(name='YO', value='FUN')
        await interaction.response.edit_message(embed=wplist(1))



@bot.command()
async def menu(ctx):
    view = Menu()

    # embed = discord.Embed(title='WP Menu', color=discord.Color.dark_purple)
    embed = wplist()


    await ctx.reply(embed=embed, view=view)


@bot.command()
async def list(ctx, mode=0):
    embed = wplist(mode)
    await ctx.reply(embed = embed)

@bot.command()
async def add(ctx, *, args):
    title = args[:args.index(" https:")]
    link = args[args.index(" https:")+1:]
    completed = False
    # await ctx.reply(args + '\n' + args[:args.index(" https:")] + '\n' + args[args.index(" https:")+1:])
    await ctx.reply(f"Sucessfully added {wpadd(title, link, completed)}")

@bot.command()
async def delete(ctx, title):
    await ctx.reply(f'Successfully deleted {wpdelete(title)}')

@bot.command()
async def complete(ctx, title):
    await ctx.reply(f'Congrats on completing {wpcomplete(title)}!')

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