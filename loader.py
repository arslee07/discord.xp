from sqlite3 import connect
import pymysql as mysql,os,time
from discord.ext import commands 

connection = mysql.connect(
    host="127.0.0.1",
    user="root",
    password="?",
    database="xpdata"
)

token = "your awesome token :+1:"
with connection:
    cursor = connection.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS usersData(
        userId VARCHAR(255),
        guildId VARCHAR(255),
        xpValue VARCHAR(255)
        );""")
    client = commands.Bot(command_prefix='xp/')
    client.cursor = cursor
    client.connection = connection
    for cog in os.listdir('cogs'):
        if cog.endswith(".py"):
            client.load_extension(f'cogs.{cog[:-3]}')
            print(cog)
    
    
    client.run(token)
    
