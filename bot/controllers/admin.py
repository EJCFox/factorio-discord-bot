import logging
from discord.ext import commands
from ..services.channelMappingService import ChannelService
from ..services.gameService import GameService

class Admin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.channels = ChannelService()
    self.games = GameService()

  @commands.Cog.listener()
  async def on_ready(self):
    await self.channels.init_channel_table()

  @commands.command(help='Create a new game', usage='<name> [version]')
  async def new(self, ctx, name, *args):
    logging.info('Received command: `!new`')
    version = args[0] if len(args) > 0 else 'latest'
    try:
      await ctx.send('Creating new game :star2:')
      await self.games.create_game(name, version)
      await ctx.send('Done!')
    except:
      await ctx.send('ERROR :fire:')

  @commands.command(help='Delete a game')
  async def delete(self, ctx, name):
    logging.info('Received command: `!delete`')
    try:
      await ctx.send('Deleting the game')
      await self.games.delete_game(name)
      await ctx.send("Done!")
    except:
      await ctx.send('ERROR :fire:')

  @commands.command(help='List all active games')
  async def list(self, ctx):
    logging.info('Received command: `!list`')
    stacks = await self.games.list_games()
    if (len(stacks) == 0):
      await ctx.send('There are no games at the moment. Create a new one with `!new`.')
      return
    for stack in stacks:
      await ctx.send(stack['StackName'] + ': ' + stack['StackStatus'])

  @commands.command(name="set-game", help='Link the current channel to the specified game')
  async def set_game(self, ctx, name):
    logging.info('Received command: `!set_game`')
    if await self.games.game_exists(name):
      await self.channels.set_channel_mapping(name, ctx.channel.guild.id, ctx.channel.id)
      await ctx.send(f'This channel will now control game `{name}` :tada:')
    else:
      await ctx.send('Sorry, I did not recognise that game :confused:')

