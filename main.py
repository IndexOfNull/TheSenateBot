import asyncio
import discord
import sys, os
import json
from bot import SWBot

with open("bot.json","r") as f:
  settings = json.loads(f.read())

bot_token = settings["bot_token"]

loop = asyncio.get_event_loop()

bot = SWBot(token=bot_token)

if __name__ == "__main__":
	try:
		task = loop.create_task(bot.run())
		task.add_done_callback(functools.partial(main, loop))
		bot.own_task = task
		#loop.create_task(watcher())
		loop.run_until_complete(task)
		loop.run_forever()
	except (KeyboardInterrupt, RuntimeError):
		print('\nKeyboardInterrupt - Shutting down...')
		bot.die()
	finally:
		print('--Closing Loop--')
		loop.close()
