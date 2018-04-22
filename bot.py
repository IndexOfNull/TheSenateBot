import asyncio
import discord
from discord.ext import commands
import sys, os

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

	async def on_ready(selfs):
		print("READY!")

	async def on_message(self,message):
		print("Message!")
		await self.process_commands(message)

	def run(self):
		super().run(self.token)

	def die(self):
		try:
			self.loop.stop()
			self.loop.run_forever()
		except Exception as e:
			print(e)
