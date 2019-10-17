from MarbleManager import marbleManager

commands = [
    "**help:** you just used it", 
    "**ping:** pong", 
    "**register:** register and recieve a random amount of marbles from 20 to 40",
    "**profile:** shows your current marble amount",
    "**coinflip [x]:** bets x marbles on a 50/50",
    "**leaderboard [x]:** where x is attribute (like marbles)"
    ]

async def processCommand(message, commandPrefix, client):
    command = message.content[1:] #the message without the commandPrefix
    
    if command == "help":
        helpMessage = ""
        for x in commands:
            helpMessage += x + "\n\n"
        await message.channel.send(helpMessage)
        
    elif command == "ping":
        await message.channel.send("pong")
        
    elif command == "register":
        await marbleManager.register(message.author, message.channel)
        
    elif command == "profile":
        await marbleManager.getCollection(message.author, message.channel)
        
    elif command.split()[0] == "coinflip":
        parts = command.split()
        if len(parts) == 2:
            if not parts[1].isdigit():
                await message.channel.send("You didn't specify a number correctly dumbo.")
            else:
                #good to go
                await marbleManager.coinflip(message.author, message.channel, int(parts[1]))
        else:
            await message.channel.send("coinflip should have 2 parts seperated by a space dumbass.")
            
    elif command.split()[0] == "leaderboard":
        parts = command.split()
        if len(parts) == 2:
            await marbleManager.leaderboard(message.author, message.channel, parts[1], client)
        else:
            await message.channel.send("leaderboard should have 2 parts seperated by a space dumbass.")    
        
    else:
        await message.channel.send("Command not recognized. " + commandPrefix + "help to see commands.")