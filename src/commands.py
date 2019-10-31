from MarbleManager import marbleManager

commands = [
    "**help:** you just used it", 
    "**ping:** pong", 
    "**register:** register and recieve a random amount of marbles from 20 to 40",
    "**profile:** shows your current marble amount",
    "**coinflip [x]:** bets x marbles on a 50/50",
    "**leaderboard [x]:** where x is attribute (like marbles)",
    "**give [x] [@user]:** where x is amount of marbles to give"
    ]

async def timedReward(client):
    await marbleManager.dailyReward(client)

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
            await message.channel.send("coinflip should have 2 parts seperated by a space dumbo.")
            
    elif command.split()[0] == "leaderboard":
        parts = command.split()
        if len(parts) == 2:
            await marbleManager.leaderboard(message.author, message.channel, parts[1], client)
        else:
            await message.channel.send("leaderboard should have 2 parts seperated by a space dumbo.")  
            
    elif command.split()[0] == "give":
        parts = command.split()
        if len(parts) == 3:
            if parts[1].isdigit():
                await marbleManager.give(message.author, message.channel, int(parts[1]), message.mentions[0])
            elif parts[2].isdigit():
                await marbleManager.give(message.author, message.channel, int(parts[2]), message.mentions[0])
            else:
                await message.channel.send("You didn't specify a number correctly dumbo.")
        else:
            await message.channel.send("give should have 3 parts.")
            
    elif command.split()[0] == "cooltext":
        userInput = command[len(command.split()[0])+1:]
        output = ""

        for x in range(len(userInput), 0, -1):
            blah=" "*x + userInput[x:len(userInput)-x]
            if userInput[x:len(userInput)-x] != "":
                output+=blah+"\n"

        for x in range(len(userInput)):
            blah=" "*x + userInput[x:len(userInput)-x]
            if userInput[x:len(userInput)-x] != "":
                output+=blah+"\n"

        await message.channel.send("```\n" + output + "```")    
        
    else:
        await message.channel.send("Command not recognized. " + commandPrefix + "help to see commands.")