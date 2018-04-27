import asyncio
import discord
import aiohttp
import async_timeout
import json


class funcs():

	def __init__(self):
		print("Initialized functions")
		self.session = aiohttp.ClientSession()

	async def http_get_json(self, url, **kwargs):
		headers = kwargs.pop("headers",{})
		try:
			with async_timeout.timeout(10):
				async with self.session.get(url,headers=headers) as resp:
					data = json.loads(await resp.text())
					return data
		except asyncio.TimeoutError:
			return False
		except Exception as e:
			print(e)
			return False

	async def imgurToImageUrl(self,id):
		if id.startswith("http"):
			id = id.split("/")[-1]
			stripped_extentions = [".jpg",".jpeg",".gif",".png"]
			for ext in stripped_extentions:
				id = id.replace(ext,"")
		imgur_url = "https://i.imgur.com/{0}.jpg".format(id)
		print(imgur_url)
		try:
			with async_timeout.timeout(10):
				async with self.session.get(imgur_url) as resp:
					if resp.status == 200:
						return imgur_url
		except asyncio.TimeoutError:
			return None
		except Exception as e:
			print(e)
			return None
		return None

	async def getReddit(self,subreddit,**kwargs):
		try:
			query = kwargs.pop("query",None)
			nsfw = kwargs.pop("nsfw",False)
			stickies = kwargs.pop("stickies",False)
			author = kwargs.pop("author",None)
			video = kwargs.pop("video",False)
			before = kwargs.pop("before",None)
			after = kwargs.pop("after",None)
			sort = kwargs.pop("sort","desc")
			size = kwargs.pop("size",60)
			spoilers = kwargs.pop("spoilers",False)
			bools = {"over_18": nsfw,"stickies":stickies,"is_video":video,"spoilers":spoilers}
			strings = {"subreddit":subreddit,"q":query,"author":author,"before":before,"after":after,"sort":sort}
			url = "https://api.pushshift.io/reddit/search/submission/"
			first = True
			for key,val in bools.items():
				if val is None:
					continue
				if first:
					url += "?{0}={1}".format(key,str(val).lower())
					first = False
				else:
					url += "&{0}={1}".format(key,str(val).lower())
			for key,val in strings.items():
				if val is None:
					continue
				if first:
					url += "?{0}={1}".format(key,val)
				else:
					url += "&{0}={1}".format(key,val)
			response = await self.http_get_json(url)
			return response
		except:
			return None
