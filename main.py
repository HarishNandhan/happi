#this branch is repl only version
import discord
import os
import datetime
import reply
import cricket
from keep_alive import keep_alive

client = discord.Client(description='hp help')

cric_on = False
match = 0

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
    if message.content.lower().startswith('hp cricket') or cric_on:
        if message.content.lower().startswith('hp cricket') and cric_on:
            await message.channel.send('Already game is going on\nPlease wait untill the game is over.')
        elif message.content.lower().startswith('hp cricket'):
            match = cricket.cric(message)
            if match.check():
                cric_on = True
                await message.channel.send(match.ready())
            else:
                await message.channel.send('Same player cant play in two teams\nAlso bot name cant be mentioned!')
        if message.content.lower()=='send':
            for player in match.players:    
                user = await client.fetch_user(player.id)
                await user.send('hello man!')
                print('opssss')
    #hp basic reply
    elif message.content.lower().startswith('hp') or str(message.channel).startswith('Direct') or str(message.channel)=='hp-here':
        msg = get_msg(message)
        t = message.created_at + datetime.timedelta(hours=5, minutes=30)
        print(message.channel)
        await message.channel.send(reply.reply(msg, message, t))
    #vote function
    elif message.contect.lower().startswith('vote'):
        await message.add_reaction(':thumbsup:')
        await message.add_reaction(':thumbsdown:')

keep_alive()
client.run(os.environ['TOKEN'])
