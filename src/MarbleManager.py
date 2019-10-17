import random
import shelve

class MarbleManager:
    
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
            
marbleManager = MarbleManager()