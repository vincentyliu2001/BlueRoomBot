import os
import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import urllib.request



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
newsletters_link = 'https://us2.campaign-archive.com/home/?u=62d875b2e6699fa3d515416eb&id=850b201247'

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    print(message.content)
    if message.content.find("!newsletter") != -1:
        command = message.content
        if command == "Usage: !newsletter [space] <newsletter number>":
            return
        try:
            newsletter_number = int(command.split()[1])
        except (ValueError, IndexError) as e:
            await message.channel.send("Usage: !newsletter <newsletter number>")
        search = 'Blue Room Weekend Update #' + "{0:0=3d}".format(newsletter_number)
        print(search)
        fp = urllib.request.urlopen(newsletters_link)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        print(mystr)
        soup = BeautifulSoup(mystr, 'html.parser')
        for tag in soup.find_all("a", text=search):
            await message.channel.send(tag['href'])
            return
        issue_count = len(soup.find_all("li", {"class": "campaign"}))
        await message.channel.send('This newsletter has not been released yet! The most recent issue is #' +
                                   "{0:0=3d}".format(issue_count))
client.run(TOKEN)
