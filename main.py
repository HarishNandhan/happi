import discord
import os
import datetime
import reply
import cricket
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

match = cricket.cric(0)

def get_msg(message):
    msg = message.content.lower()
    msg = [wr for wr in msg.split(' ') if wr!='']
    if msg[0]=='hp':
        msg.pop(0)
    msg = ' '.join(msg)
    return msg

@client.event
async def on_message(message):
    global cric_on, match
    #dont care
    if message.author == client.user or message.content.startswith('-'):
        return
    #hand cricket functions
    if message.content.lower().startswith('hp cricket') or match.cric_on:
        if message.content.lower().startswith('hp cricket') and match.cric_on:
            await message.channel.send('Already game is going on\nPlease wait untill the game is over.')
        elif message.content.lower().startswith('hp cricket'):
            match = cricket.cric(message)
            await match.channel.send(match.check())
        elif message.content.lower().startswith('hp start'):
            author = message.author
            if author in match.players and author not in match.start_lis:
                await match.channel.send(match.start(author))
                if len(match.players)==len(match.start_lis):
                    thing = match.begin()
                    for player in match.players:    
                        user = await client.fetch_user(player.id)
                        await user.send(thing)
        elif str(message.channel).startswith('Direct') and message.author in match.players:
            try:
                sign = int(message.content)
                if 0<sign<7:
                    thing = match.play(sign, message)
                    if match.status=='played':
                        for player in match.players:    
                            user = await client.fetch_user(player.id)
                            await user.send(thing)
                    else:
                        await message.channel.send('waiting for other player')
                else:
                    await message.channel.send('Enter a number form 1 to 6')
            except ValueError:
                await message.channel.send('Enter a number')

    #hp exam focus comments
    elif message.content.lower().startswith('hp focus') and str(message.channel)=='lobby':
        msg = get_msg(message)[6:]
        member = message.author
        if msg=='none':
            for i in range(10):
                var = discord.utils.get(message.guild.roles, name = str(i))
                await member.remove_roles(var)
        elif msg=='all':
            for i in range(10):
                var = discord.utils.get(message.guild.roles, name = str(i))
                await member.add_roles(var)
        else:
            var = discord.utils.get(message.guild.roles, name = msg)
            await member.add_roles(var)
        await message.add_reaction('\N{THUMBS UP SIGN}')
    #hp basic reply
    elif message.content.lower().startswith('hp') or str(message.channel).startswith('Direct') or str(message.channel)=='hp-here':
        msg = get_msg(message)
        t = message.created_at + datetime.timedelta(hours=5, minutes=30)
        print(message.channel)
        await message.channel.send(reply.reply(msg, message, t))
    #vote function
    elif message.contect.lower().startswith('vote'):
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.add_reaction('\N{THUMBS DOWN SIGN}')

client.run(os.environ['TOKEN'])
