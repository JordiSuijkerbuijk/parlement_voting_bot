import os

import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
  print(
    f'{bot.user} is connected'
  ) 

@bot.command(name='create_parlement')
async def create_parlement(ctx, arg: None):
  if arg is None:
    await ctx.send('This parlement needs a name, provide this by adding a value after the command')
    return 

  guild = ctx.guild
  if get(ctx.guild.roles, name=arg):
    await ctx.send('This parlement already exists, join this parlement by asking the president')

  DEFAULT_PERMISSIONS = os.getenv('DEFAULT_PERMISSIONS')
  permission = discord.Permissions(permissions = 1071862243137)

  await guild.create_role(name=arg, permissions=permission)

  await ctx.send(f'parlement {arg} has been created')
  return 

@bot.command(pass_context=True, name='join_parlement')
@commands.has_role("1337")
async def join_parlement(ctx, user: discord.Member, role: discord.Role):
  if role is None:
    await ctx.send("This parlement doesn't exists, join a parlement that exists")
    return

  if user is None:
    await ctx.send("What user should be added to the parlement?")
    return

  await user.add_roles(role)

  await ctx.send(f'{user.name} has been added to {role.name}')
  return

@bot.command(pass_context=True, name='poll')
async def create_poll(ctx, question: str = None):
  if question is None:
    await ctx.send("The poll needs a yes or no question.")
    return

  #TODO add @channel command when adding to moccamasters 
  message = await ctx.send(f"``` New poll: {question} \n\n✅ = Yes \n❎ = No \n\n Verdict will be within 2 minutes ```")
  await message.add_reaction('✅')
  await message.add_reaction('❎')

  #more votes than amount of roles needed
  time.sleep(5)

  reactions = await ctx.channel.fetch_message(message.id)
  yes = get(reactions.reactions, emoji=':white_check_mark:')
  print(reactions)

  return

@bot.command(name='end_poll')
async def end_poll(ctx, arg=None):
  return

@bot.command(name='vote_kick')
async def vote_kick_from_parlement(ctx, arg=None):
  return

@bot.command(name='set_color')
async def set_color(ctx, arg=None):
  return

#error catching
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
    await ctx.send(f'{error}')


bot.run(TOKEN)