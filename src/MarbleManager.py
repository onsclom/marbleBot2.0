import random
import shelve

class MarbleManager:

    def __init__(self):
        self.marbleRecords = shelve.open("data", writeback=True)
    
    async def register(self, author, channel):
        server = str(channel.guild.id) 
        if server not in self.marbleRecords: #if server doesn't have record
            self.marbleRecords[server]={} #create new empty dict
            
        if author.id in self.marbleRecords[server]: 
            await channel.send("You are already registered dummy.")
        else: 
            randomAmount = random.randrange(20,41,1) #20 to 40 inclusive
            self.marbleRecords[server][author.id] = randomAmount
            name = author.name if author.nick == None else author.nick
            await channel.send( str(name) + " has registered and recieved " + str(randomAmount) + " marbles" + ("!" if randomAmount>=38 else ".") )
            
    async def getCollection(self, author, channel):
        server = str(channel.guild.id)
        if server not in self.marbleRecords or author.id not in self.marbleRecords[server]:
            await channel.send("You are not registered dummy.") 
        else:
            userAmount = self.marbleRecords[server][author.id]
            name = author.name if author.nick == None else author.nick
            await channel.send( str(name) + ": " + str(userAmount) + (" marble." if userAmount==1 else " marbles.") )     
            
    async def coinflip(self, author, channel, bet):
        server = str(channel.guild.id)
        name = author.name if author.nick == None else author.nick
        if self.marbleRecords[server][author.id] >= bet:
            outcome = random.choice([0,1])
            if outcome == 1:
                await channel.send( str(name) + " won " + str(bet) + (" marble." if bet==1 else " marbles.") )
                self.marbleRecords[server][author.id] += bet
            else:
                await channel.send( str(name) + " lost " + str(bet) + (" marble." if bet==1 else " marbles.") )
                self.marbleRecords[server][author.id] -= bet
        else:
            await channel.send("why you trying to break my bot")
marbleManager = MarbleManager()