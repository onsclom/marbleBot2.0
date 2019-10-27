import os
import discord
from dotenv import load_dotenv
from commands import processCommand, timedReward

commandPrefix = "!"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await timedReward(self)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))     
        if message.content[0] == commandPrefix:
            await processCommand(message, commandPrefix, client)

client = MyClient()
client.run(token)