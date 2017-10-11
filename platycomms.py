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

#if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    #discord.opus.load_opus('opus')
discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')

client = discord.Client()

voice_clients = {}
voice_channels = {}
clients = []
stream_player = None

@client.event
async def on_ready():
    logger.info('Logged in as %s/%s' % (client.user.name, client.user.id))

    channels = client.get_all_channels()
    for channel in channels:
        if channel.type == ChannelType.voice:
            if channel.name == config['channel_name']:
                voice_clients[channel.server.name] = await client.join_voice_channel(channel)
                voice_channels[channel.server.name] = channel


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
            members = v.voice_members
            in_channel = False
            for m in members:
                if m.name == j['player_name']:
                    in_channel = True
                    break
            if in_channel == True:
                if j['command'] in ['hello', 'jump_check', 'its_me', 'im_down', 'im_dead', 'hes_down', 'hes_dead', 'north', 'south', 'east', 'west', 'yes', 'no']:
                   folder = '/var/www/dandelopia/plat/audio/' + j['command'] + '/'
                   filename = random.choice(os.listdir(folder))
                   full_path = folder + filename
                   vc = voice_clients[j['server_name']]
                   global stream_player
                   if stream_player is None or (stream_player is not None and not stream_player.is_playing()):
                       stream_player = vc.create_ffmpeg_player(full_path)
                       stream_player.volume = 0.6
                       stream_player.start()
                   else:
                       logger.info("Not playing, already busy")
                else:
                   logger.info("Command not found: " + j['command'])
            else:
                logger.info("User not in channel: " + j['player_name'])
        else:
            logger.info("secret key does not match: " + j['secret_key'])
        
    def connection_lost(self, ex):
        clients.remove(self)


coro = client.loop.create_server(SimpleServer, host='127.0.0.1', port=int(config['listen_port']) or 1234)
server = client.loop.run_until_complete(coro)
logger.info("We got port: " + config['listen_port'])
for socket in server.sockets:
    logger.info("serving on {}".format(socket.getsockname()))
logger.info("invoke on otoken: " + config['token'])
client.run(config['token'])

