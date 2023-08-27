
import getServerInfo

import asyncio
import time
import datetime
import json
import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks

if not os.path.isfile("servers.txt"):
	open("servers.txt",'w').close()
servers = open('servers.txt','r').readlines()

token = "MTEwNDIxMzY1NzcyMzg2NzIwNw.GOr85W.Fgv8CbdCax7jMaXoCgtsMqt5c8CsdBjM1T9xPY"

imgDir = "images/"

cooldown = 5*60

client = commands.Bot(command_prefix="!!!!!", intents = discord.Intents.default())
client.owner_id = 280804464355573770

#class MyClient(discord.Client):
#	async def on_ready(self):
#		print("Logged in as {}".format(self.user))
#		owner = await self.fetch_user(280804464355573770)
#		if owner != None:
#			await owner.send("Ayo! Bot online!")
#			await owner.send("Current servers: {}".format(servers))
#		else:
#			print("Bad user id")


#	@client.command(name="testcommand")
#	async def testcommand(interaction: discord.Interaction, message: discord.Message):
#		await interaction.send_message(content="it Worked!")

updateStuff = []

def updateServers():
	updateStuff = []
	if os.stat("servers.txt").st_size != 0:
		file = open("servers.txt", 'r')
		for x in file.readlines():
#			print("ayo {}".format(x))
			x = x.split("\t")
			updateStuff.append([x[0],x[1],x[2].strip("\n")])
#		print("Persistent messages updated! {}".format(updateStuff))
#	else:
#		print("No persistent messages to update")
	return updateStuff

loop = asyncio.new_event_loop()
async def updateMessages():
	while True:
		updateStuff = updateServers()
#		print("messages updating: {}".format(updateStuff))
		if len(updateStuff) > 0:
			for x in updateStuff:
				if x[0] != '-1':
					ip = x[0]
					status = getServerInfo.getInfo(ip)
					if status != None:
						getServerInfo.getImage(ip)
						img = discord.File(imgDir + "image.png")
						embed = discord.Embed()
						embed.color = discord.Color.green()
						players = ""
						isOk = True
						if status["players"]["online"] > 0:
							for i in range(len(status["players"]["sample"])):
								temp = status["players"]["sample"][i]["name"]
								if temp.startswith('.'):
									temp = temp[1:]
								players = players + temp
								if i+1 < len(status["players"]["sample"]):
									players = players + ", "
								if not status["players"]["sample"][i]["name"].isalnum() and not status["players"]["sample"][i]["name"].startswith('.'):
									isOk = False
#								print("Length: {}".format(len(players)))
						if len(players) != 0 and isOk:
							if len(status["players"]["sample"]) < status["players"]["online"]:
								players = players + " + {} others.".format(status["players"]["online"] - len(status["players"]["sample"]))
							embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: {4}".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"], players)
						elif status["players"]["online"] == 0:
							embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: None".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"])
						else:
							embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: Not Available".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"])
#						embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: {4}".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"], players)
						embed.title="Server is Online!"
						embed.set_thumbnail(url="attachment://image.png")
#						if len(status["players"
						img = discord.File(imgDir + "image.png")
					else:
						embed = discord.Embed()
						embed.color = discord.Color.red()
						embed.title="Server is unreachable!"
						embed.description = "The server `{}` is either offline, or it doesn't exist.".format(ip)
						img = discord.File(imgDir + "fail.png")
						embed.set_thumbnail(url=f"attachment://fail.png")
#					embed.set_footer(text="Last updated: <t:{:.0f}:R>".format(time.time()))
					embed.timestamp = datetime.datetime.utcnow()
					channel = await client.fetch_channel(x[2])
					msg = await channel.fetch_message(x[1])
#					print("Message content: {}".format(msg.content))
					await msg.edit(embed=embed, content="", attachments=[img])
		await asyncio.sleep(cooldown)
	

@client.event
async def on_ready():
	owner = await client.fetch_user(client.owner_id)
#	await owner.send("Ayo 2!")
#	print("It worked maybe")
	await client.tree.sync()
#	print("Commands Synced")
#	updateStuff = []
	updateServers()
#	if len(updateStuff) > 0:
#		print("Servers: {}".format(updateStuff))
#	else:
#		print("No servers being updated")
	asyncio.ensure_future(updateMessages())
#	asyncio.set_event_loop(updateMessages())
	loop.run_forever
	print("Bot successfully connected to {0} at {1}:{2}".format(client.user.display_name, datetime.time().hour, datetime.time().minute))

@client.tree.command(name="testcommand", description="don't use, or do.")
async def testcommand(interaction: discord.Interaction):
	await interaction.response.send_message("No, you're a test", ephemeral=True)

@client.tree.command(name="serverstatus", description="Check on the status of a server!")
@app_commands.describe(ip="IP to get the status of")
async def serverstatus(interaction: discord.Interaction, ip: str):
	status = getServerInfo.getInfo(ip)
	
	if status != None:
		getServerInfo.getImage(ip)
		img = discord.File(imgDir + "image.png")
		embed = discord.Embed()
		embed.color = discord.Color.green()
		players = ""
		isOk = True
		if status["players"]["online"] > 0:
			for x in range(len(status["players"]["sample"])):
				temp = status["players"]["sample"][x]["name"]
				if temp.startswith('.'):
					temp = temp[1:]
				players = players + temp
				if x+1 < len(status["players"]["sample"]):
					players = players + ", "
				if not status["players"]["sample"][x]["name"].isalnum() and  not status["players"]["sample"][x]["name"].startswith('.'):
					isOk = False
#			print("Length: {}".format(len(players)))
		if len(players) != 0 and isOk:
			if len(status["players"]["sample"]) < status["players"]["online"]:
				players = players + " + {} others.".format(status["players"]["online"] - len(status["players"]["sample"]))

			embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: {4}".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"], players)
		elif status["players"]["online"] == 0:
			embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: None".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"])
		else:
			embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: Not Available".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"])
#		embed.description = "IP: {0}\nVersion: {1}\nPlayers count: {2}/{3}\nPlayers: {4}".format(ip,status["version"]["name"],status["players"]["online"],status["players"]["max"], players)
		embed.title="Server is Online!"
		embed.set_thumbnail(url=f"attachment://image.png")
#		if len(status["players"
	else:
		embed = discord.Embed()
		embed.color = discord.Color.red()
		embed.title="Server is unreachable!"
		embed.description = "The server `{}` is either offline, or it doesn't exist.".format(ip)
		img = discord.File(imgDir + "fail.png")
		embed.set_thumbnail(url=f"attachment://fail.png")
#	embed.set_footer(text="Last updated: <t:{:.0f}:R>".format(time.time()))
	embed.timestamp = datetime.datetime.utcnow()
	await interaction.response.send_message(embed= embed, file=img)

@client.tree.command(name="watchserver", description="will create a permanent message to constantly update a server's status")
@app_commands.describe(ip="IP to keep updates for", channel_id="Which channel to put the message in. Use \"here\" for the current channel")
async def watchserver(interaction: discord.Interaction, ip: str, channel_id: str):
#	print("start")
	if channel_id == "here":
		channel_id = interaction.id
	try:
		Channel = await client.fetch_channel(channel_id)
	except NotFound:
		await interaction.response.send_message("Invalid Channel ID!", ephemeral=True)
	try:
		msgID = await Channel.send("Awaiting update!")
	except Forbidden:
		await interaction.response.send_message("Unable to send a message in that channel! Do I not have permission? :(", ephemeral=True)
	with open("servers.txt", "r+") as file:
		lines = file.readlines()
		lines = lines[:-1]
#		file.write(lines)

	file = open("servers.txt",'a')
	for i in lines:
		file.write(i)
	file.write("{}\t{}\t{}\n".format(ip,msgID.id,channel_id))
	file.write("-1\t-1\t-1")
	file.close()
	print("done")
	updateServers()
	await interaction.response.send_message("Message Sent!", ephemeral=True, delete_after=60)

@client.tree.command(name="serverjson")
@app_commands.describe(ip="IP for the json obtaining")
async def serverjson(interaction: discord.Interaction, ip: str):
	status = getServerInfo.getInfo(ip)
	if status != None:
		try:
			await interaction.response.send_message("Json response from {0}:\n{1}".format(ip,status))
		except discord.errors.HTTPException:
			await interaction.response.send_message("Error: json too long! Go to <https://api.mcstatus.io/v2/status/java/{0}>".format(ip), ephemeral=True)
	else:
		await interaction.response.send_message("Error: No server found. Either the server is offline, or check the IP and try again", ephemeral=True, delete_after=30)

@client.tree.command(name="removestatus", description="Remove messages from updates")
@app_commands.describe(message_id="Message ID to remove from updates (use * to remove all)")
async def removestatus(interaction: discord.Interaction, message_id: str):
	if channel_id == '*':
		file = open("servers.txt",'w')
		file.close()
		updateServers()
		await interaction.response.send_message("All update messages have been removed from memory!")
	else:
		with open("servers.txt", 'r') as file:
			lines = file.readlines()
		with open("servers.txt", 'w') as file:
			content = ""
			for x in lines:
				temp = x
				x.strip("\n")
				x = x.split("\t")
				if x[1] != message_id:
					file.write(temp)
		await interaction.response.send_message("Message has been removed from updates!")

@client.tree.command(name="help", description="display the list of commands, and their uses")
async def help(interaction: discord.Interaction):
	embed = discord.Embed()
	embed.color = discord.Color.blue()
	embed.title = "Minecraft Server Bot Help!"
	embed.description = "This bot is designed to allow you to easily check the status of different minecraft servers!\n**__Commands:__**\n> /serverstatus - check the status of a server\n> /watchserver - create an automatically-updating message, displays the same info as /serverstatus\n> /removestatus - tells the bot to stop updating the message set from /watchserver\n> /serverjson - get the raw json status from a server"
	embed.set_footer(text="Created by Nathan Fullerton")
	embed.set_thumbnail(url=client.user.avatar.url)
	await interaction.response.send_message(embed=embed, ephemeral = True)

if __name__ == "__main__":
#	await client.tree.sync()
	client.run(token)

