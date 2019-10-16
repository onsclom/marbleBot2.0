import os
import discord
from dotenv import load_dotenv
from commands import processCommand

commandPrefix = "!"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))     
        if message.content[0] == commandPrefix:
            await processCommand(message, commandPrefix)

client = MyClient()
client.run(token)