import random
import shelve
import discord
import asyncio

class MarbleManager:
    
    async def dailyReward(self, client):
        rewardAmount = 1 # Amount to give
        interval = 60 * 60 * 1 #hours
        while True:
            await asyncio.sleep(interval)
            print("rewarding now!")
            for server in client.guilds:
                marbleRecords = shelve.open(str(server.id), writeback=True)
                for x in marbleRecords:
                    marbleRecords[x]["marbles"] = marbleRecords[x]["marbles"] + rewardAmount
                    print(marbleRecords[x]["marbles"], "to", marbleRecords[x]["marbles"] + rewardAmount)
                marbleRecords.close()  
    
    async def register(self, author, channel):
        server = str(channel.guild.id) 
        marbleRecords = shelve.open(server, writeback=True) #open server DB

        if str(author.id) in marbleRecords: 
            await channel.send("You are already registered dummy.")
        else: 
            randomAmount = random.randrange(20,41,1) #20 to 40 inclusive
            marbleRecords[str(author.id)] = {}
            marbleRecords[str(author.id)]["marbles"] = randomAmount
            name = author.name if author.nick == None else author.nick
            await channel.send( str(name) + " has registered and recieved " + str(randomAmount) + " marbles" + ("!" if randomAmount>=38 else ".") )
            
    async def getCollection(self, author, channel):
        server = str(channel.guild.id)
        marbleRecords = shelve.open(server)
        if not str(author.id) in marbleRecords:
            await channel.send("You are not registered dummy.") 
        else:
            userAmount = marbleRecords[str(author.id)]["marbles"]
            name = author.name if author.nick == None else author.nick
            await channel.send( str(name) + ": " + str(userAmount) + (" marble." if userAmount==1 else " marbles.") )     
            
    async def coinflip(self, author, channel, bet):
        server = str(channel.guild.id)
        marbleRecords = shelve.open(server, writeback=True)
        name = author.name if author.nick == None else author.nick
        if marbleRecords[str(author.id)]["marbles"] >= bet:
            outcome = random.choice([0,1])
            if outcome == 1:
                await channel.send( str(name) + " won " + str(bet) + (" marble." if bet==1 else " marbles.") )
                marbleRecords[str(author.id)]["marbles"] += bet
            else:
                await channel.send( str(name) + " lost " + str(bet) + (" marble." if bet==1 else " marbles.") )
                marbleRecords[str(author.id)]["marbles"] -= bet
        else:
            await channel.send("why you trying to break my bot")
    
    async def leaderboard(self, author, channel, attribute, client):
        server = str(channel.guild.id)
        marbleRecords = shelve.open(server, writeback=True)
        contendors = []
        for x in marbleRecords:
            if attribute in marbleRecords[x]:
                curUser = channel.guild.get_member(int(x))
                if curUser != None: #if the user exists in the server
                    name = curUser.name if curUser.nick == None else curUser.nick
                    contendors.append((name, marbleRecords[x][attribute]))
        
        if len(contendors):
            currentEmbed = discord.Embed(title=attribute + " Leaderboard", color=0x50bdfe)
            
            contendors.sort(key=lambda tup: tup[1], reverse=True)
            
            names = ""
            marbles = ""
            for x in range(len(contendors)):
                names += str(x+1) + ". " + contendors[x][0] + "\n"
                marbles += str(contendors[x][1]) + "\n"
            
            currentEmbed.add_field(name="Names", value=names, inline=True)
            currentEmbed.add_field(name="Marbles", value=marbles, inline=True)
            
            await channel.send(embed=currentEmbed)
        else:
            await channel.send("Nobody has statistics for " + attribute)
            
    async def give(self, author, channel, amount, other):
        server = str(channel.guild.id)
        marbleRecords = shelve.open(server, writeback=True)
        if str(author.id) in marbleRecords and str(other.id) in marbleRecords:
            if marbleRecords[str(author.id)]["marbles"] >= amount:
                marbleRecords[str(author.id)]["marbles"] -= amount
                marbleRecords[str(other.id)]["marbles"] += amount
                giverName = author.name if author.nick == None else author.nick
                receiverName = other.name if other.nick == None else other.nick
                await channel.send(giverName + " gives " + receiverName + " " + str(amount) + (" marble." if amount==1 else " marbles."))
            else:
                await channel.send("You do not have enough marbles")
        else:
            await channel.send("Someone isn't registered.")
        
marbleManager = MarbleManager()