from MarbleManager import marbleManager

commands = ["help", "ping"]

async def processCommand(message, commandPrefix):
    command = message.content[1:] #the message without the commandPrefix
    
    if command == "help":
        helpMessage = "```\n"
        for x in commands:
            helpMessage += x + "\n"
        helpMessage += "```"
        await message.channel.send(helpMessage)
        
    elif command == "ping":
        marbleManager.helloWorld()
        await message.channel.send("pong")
    
    else:
        await message.channel.send("Command not recognized. " + commandPrefix + "help to see commands.")