import asyncio
import discord
from discord.ext import commands
import sys, os
from util import checks
from util import funcs

modules = [
"cogs.main"
]

def init_funcs(bot):
	bot.funcs = funcs.funcs()

class SWBot(commands.AutoShardedBot):

	def __init__(self,*args,**kwargs):
		if sys.platform == "win32":
			self.loop = kwargs.pop('loop', asyncio.ProactorEventLoop())
			asyncio.set_event_loop(self.loop)
		else:
			self.loop = kwargs.pop('loop', asyncio.get_event_loop())
			asyncio.get_child_watcher().attach_loop(self.loop)
		self.token = kwargs.pop("token")
		command_prefix = kwargs.pop('command_prefix', commands.when_mentioned_or('+'))
		max_messages = kwargs.pop('max_messages',5000)
		super().__init__(command_prefix=command_prefix, *args, **kwargs)

	async def on_ready(self):
		print("READY!")
		init_funcs(self)
		for cog in modules:
			try:
				self.load_extension(cog)
			except Exception as e:
				msg = 'Failed to load mod {0}\n{1}: {2}'.format(cog, type(e).__name__, e)
				print(msg)

	async def on_message(self,message):
		print("Message!")
		await self.process_commands(message)

	async def on_command_error(self, ctx, e):

		if isinstance(e, commands.CommandNotFound):
			return
		elif isinstance(e, commands.CommandOnCooldown):
			msg = "The time to use this command has not come yet."
			await ctx.send(msg)
		elif isinstance(e, checks.No_Owner):
			msg = "You are not the senate."
			await ctx.send(msg)
		elif isinstance(e, commands.MissingRequiredArgument):
			await self.command_help(ctx)
		elif isinstance(e, commands.BadArgument):
			await self.command_help(ctx)
		elif isinstance(e, checks.No_Mod):
			msg = "This command is not for the jedi scum. (Mod perms needed)"
			await ctx.send(msg)
		elif isinstance(e, checks.No_Admin):
			msg = "This command is only for members of the senate. (Admin perms needed)"
			await ctx.send(msg)
		elif isinstance(e, commands.CheckFailure):
			msg = "The senate is collapsing. (Check failure, please ensure the bot has the proper permission for use)"
			await ctx.send(msg)
		elif isinstance(e, discord.errors.Forbidden):
			msg = "I am not the senate? (Forbidden error)"
			await ctx.send(msg)
		else:
			print("ERROR: " + str(e))

	def run(self):
		super().run(self.token)

	def die(self):
		try:
			self.loop.stop()
			self.loop.run_forever()
		except Exception as e:
			print(e)
