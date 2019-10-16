from MarbleManager import marbleManager

commands = [
    "**help:** you just used it", 
    "**ping:** pong", 
    "**register:** register and recieve a random amount of marbles from 20 to 40"
    ]

async def processCommand(message, commandPrefix):
    command = message.content[1:] #the message without the commandPrefix
    
    if command == "help":
        helpMessage = ""
        for x in commands:
            helpMessage += x + "\n"
        await message.channel.send(helpMessage)
        
    elif command == "ping":
        marbleManager.helloWorld()
        await message.channel.send("pong")
        
    elif command == "register":
        await marbleManager.register(message.author, message.channel)
        
    elif command == "collection":
        await marbleManager.getCollection(message.author, message.channel)
   
    else:
        await message.channel.send("Command not recognized. " + commandPrefix + "help to see commands.")