import asyncio
import discord
from discord.ext import commands
from random import randint
from urllib.parse import urlparse

class MainBot():

	def __init__(self,bot):
		self.bot = bot
		self.funcs = self.bot.funcs

	async def doMeme(self,sub):
		before=None
		if randint(0,1) == 1:
			before=str(randint(1,30)) + "d"
		response = (await self.bot.funcs.getReddit(sub,nsfw=False,video=False,before=before))
		if response:
			response = response["data"]
		for i in range(10):
			ind = randint(0,len(response)-1)
			post = response[ind]
			url = None
			if "url" in post:
				domain = urlparse(post["url"]).netloc
				if domain == "imgur.com":
						purl = await self.funcs.imgurToImageUrl(post["url"])
						if purl:
							url = {"url":purl,"source":post["full_link"]}
							break
			if "preview" in post:
				url = {"url":post["preview"]["images"][0]["source"]["url"],"source":post["full_link"]}
				break

		if url is None:
			await wait.edit(content=(await self.bot.funcs.getGlobalMessage(ctx.personality,"nsfw_no_search_result")))
			return
		embed = discord.Embed(title=":camera: **Source**",type="rich",color=discord.Color.purple(),url=url["source"])
		embed.set_image(url=url["url"])
		return embed

	@commands.command(aliases=["pmeme","prequel"])
	@commands.cooldown(1,3,commands.BucketType.guild)
	async def prequelmeme(self,ctx):
		try:
			embed = await self.doMeme("PrequelMemes")
			await ctx.send(embed=embed)
		except Exception as e:
			await ctx.send("`{0}`".format(e))

	@commands.command(aliases=["smeme","sequel"])
	@commands.cooldown(1,3,commands.BucketType.guild)
	async def sequelmeme(self,ctx):
		try:
			embed = await self.doMeme("SequelMemes")
			await ctx.send(embed=embed)
		except Exception as e:
			await ctx.send("`{0}`".format(e))

	@commands.command(aliases=["ememe","equel"])
	@commands.cooldown(1,3,commands.BucketType.guild)
	async def equelmeme(self,ctx):
		try:
			embed = await self.doMeme("EquelMemes")
			await ctx.send(embed=embed)
		except Exception as e:
			await ctx.send("`{0}`".format(e))

def setup(bot):
	bot.add_cog(MainBot(bot))
