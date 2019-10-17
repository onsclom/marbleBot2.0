import random
import shelve

class MarbleManager:
    async def register(self, author, channel):
        server = str(channel.guild.id) 
        marbleRecords = shelve.open('data', writeback=True)
        if server not in marbleRecords: #if server doesn't have record
            marbleRecords[server]={} #create new empty dict
            
        if author.id in marbleRecords[server]: 
            await channel.send("You are already registered dummy.")
        else: 
            randomAmount = random.randrange(20,41,1) #20 to 40 inclusive
            marbleRecords[server][author.id] = randomAmount
            name = author.name if author.nick == None else author.nick
            await channel.send( str(name) + " has registered and recieved " + str(randomAmount) + " marbles" + ("!" if randomAmount>=38 else ".") )
            
    async def getCollection(self, author, channel):
        server = str(channel.guild.id)
        marbleRecords = shelve.open('data', writeback=True)
        if server not in marbleRecords or author.id not in marbleRecords[server]:
            await channel.send("You are not registered dummy.") 
        else:
            userAmount = marbleRecords[server][author.id]
            name = author.name if author.nick == None else author.nick
            await channel.send( str(name) + ": " + str(userAmount) + (" marble." if userAmount==1 else " marbles.") )     
            
    async def coinflip(self, author, channel, bet):
        server = str(channel.guild.id)
        marbleRecords = shelve.open('data', writeback=True)
        name = author.name if author.nick == None else author.nick
        if marbleRecords[server][author.id] >= bet:
            outcome = random.choice([0,1])
            if outcome == 1:
                await channel.send( str(name) + " won " + str(bet) + (" marble." if bet==1 else " marbles.") )
                marbleRecords[server][author.id] += bet
            else:
                await channel.send( str(name) + " lost " + str(bet) + (" marble." if bet==1 else " marbles.") )
                marbleRecords[server][author.id] -= bet
        else:
            await channel.send("why you trying to break my bot")
marbleManager = MarbleManager()