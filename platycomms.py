import asyncio
import discord
import random
import os
from discord.enums import ChannelType
import json
from discord.ext import commands
from configobj import ConfigObj
import logging
import os

pid = os.getpid()
op = open("/var/run/platycomms.pid","w")
op.write("%s" % pid)
op.close()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('/var/log/platycomms.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

config = ConfigObj("/home/stevemulligan/platycomms.env")

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')
#discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')

client = discord.Client()

voice_clients = {}
voice_channels = {}
clients = []

@client.event
async def on_ready():
    logger.info('Logged in as %s/%s' % (client.user.name, client.user.id))

    for g in client.guilds:
        channels = g.voice_channels
        for channel in channels:
            if channel.name == config['channel_name']:
                #voice_clients[channel.guild.name] = await discord.VoiceChannel.connect(channel)
                voice_channels[channel.guild.name] = channel

async def join_channel(server_name, channel):
    voice_clients[server_name] = await client.join_voice_channel(channel)

async def rejoin_channel(voice_channel):
    await voice_channel.disconnect()
    voice_clients[voice_channel.guild.name] = await client.join_voice_channel(voice_channel.channel)

def get_voice_channel(voice_channel_name):
    for g in client.guilds:
        channels = g.voice_channels
        for channel in channels:
            if channel.name == voice_channel_name:
                return channel

@client.event
async def on_voice_state_update(member, before, after):
    logger.info("on_voice_state_update")
    logger.info("member: " + member.name)
    if member.name == config['member_name']:
        logger.info("before channel: " + before.channel.name)
        if (before.channel is not None and after.channel is not None):
            if (before.channel.name != config['channel_name'] and after.channel.name == config['channel_name']):
               logger.info("joined")
               voice_clients[after.channel.guild.name] = await discord.VoiceClient.connect(get_voice_channel(after.channel.name))
            elif (before.channel.name == config['channel_name'] and after.channel.name != config['channel_name']):
               logger.info("left")
               vc = voice_clients[before.channel.guild.name]
               await vc.disconnect()
               voice_clients[before.channel.guild.name] = None

        if (before.channel is not None and before.channel.name == config['channel_name']) and (after.channel is None):
           logger.info("left")
           vc = voice_clients[before.channel.guild.name]
           await vc.disconnect()
           voice_clients[before.channel.guild.name] = None
        elif before.channel is None and (after.channel is not None and after.channel.name == config['channel_name']):
           logger.info("joined")
           voice_clients[after.channel.guild.name] = await discord.VoiceClient.connect(get_voice_channel(after.channel.name))

class SimpleServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        clients.append(self)

    def data_received(self, data):
        logger.info("data_received: {}".format(data.decode()))
        j = json.loads(data.decode())
        if j['secret_key'] == config['secret_key']:
            v = voice_channels[j['server_name']]
            members = v.members
            in_channel = False
            for m in members:
                if m.name == j['player_name']:
                    in_channel = True
                    break
            if in_channel == True:
                if j['command'] in ['hello', 'jump_check', 'its_me', 'im_down', 'im_dead', 'hes_down', 'hes_dead', 'north', 'south', 'east', 'west', 'yes', 'no', 'afk', 'cancel']:
                   folder = '/var/www/dandelopia/plat/audio/' + j['command'] + '/'
                   filename = random.choice(os.listdir(folder))
                   full_path = folder + filename
                   vc = voice_clients[j['server_name']]
                   if not vc.is_connected():
                       logger.error("WTF dude, the voice client isn't connected, how could thishappen!")
                       #client.loop.create_task(join_channel(j['server_name'], v))
                   if not vc.is_playing():
                       vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(full_path), volume=0.5), after = self.done_stream)
                   else:
                       logger.info("Not playing, already busy")
                else:
                   logger.info("Command not found: " + j['command'])
            else:
                logger.info("User not in channel: " + j['player_name'])
        else:
            logger.info("secret key does not match: " + j['secret_key'])

    def done_stream(self, player):
       if player.error is not None:
           logger.error("ERROR: " + str(player.error)) 
       logger.info("We are done playing the stream") 
       #client.loop.create_task(rejoin_channel(player.vc))
        
    def connection_lost(self, ex):
        clients.remove(self)

async def periodic():
    while True:
        logger.info('periodic poll keepalive')
        for server_name, voice_client in voice_clients.items():
            logger.info('polling ' + server_name)
            voice_client.poll_voice_ws()
          
        await asyncio.sleep(60)

#asyncio.ensure_future(periodic(), loop=client.loop)

coro = client.loop.create_server(SimpleServer, host='127.0.0.1', port=int(config['listen_port']) or 1234)
server = client.loop.run_until_complete(coro)
logger.info("We got port: " + config['listen_port'])
for socket in server.sockets:
    logger.info("serving on {}".format(socket.getsockname()))
logger.info("invoke on otoken: " + config['token'])
client.run(config['token'])

