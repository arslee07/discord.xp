import discord
from discord.ext import commands,tasks

class xp(commands.Cog):
    @tasks.loop(seconds = 120)
    async def save_db(self):
        self.client.connection.commit()
    
    def __init__(self,client):
        self.client = client
        self.client.cursor = client.cursor
        self.client.connection = client.connection
        self.save_db.start()
    def cog_unload(self):
        self.save_db.stop()
        self.client.connection.commit()




    async def add_xp(self,userId,guildId,amount):


        """adding xp to member (if exists)/adding member to db and setting his xp to X"""


        self.client.cursor.execute(f"""SELECT * FROM usersData WHERE userId = {userId} AND guildId = {guildId}""")
        user = self.client.cursor.fetchone()

        if user == None:

            self.client.cursor.execute(f"""
                INSERT INTO usersData VALUES({userId},{guildId},{amount});
            """)
            return 0,amount
        else:

            total = int(user[2])+amount
            self.client.cursor.execute(f"DELETE FROM usersData WHERE userId = {userId} AND guildId = {guildId};")
            self.client.cursor.execute(f"""
                
                INSERT INTO usersData VALUES({userId},{guildId},{total});
            """)

            return user[2],total

    async def get_xp(self,userId,guildId):


        """getting xp from user"""


        self.client.cursor.execute(f"""SELECT * FROM usersData WHERE userId = {userId} AND guildId = {guildId}""")
        user = self.client.cursor.fetchone()

        if user == None:

            self.client.cursor.execute(f"""
                INSERT INTO usersData VALUES({userId},{guildId},0);
            """)
            return 0

        else:
            return user[2]


    """ xp adding (debug) """    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == self.client.user.id: return False 
        _,total = await self.add_xp(message.author.id, message.guild.id, len(message.content))
        if total/5 == round(total/5):
            await message.reply(f"xp amount: {total}")
    
    
def setup(client):
    client.add_cog(xp(client))