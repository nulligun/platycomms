import asyncio
import pprint
import discord
import random
import os
from discord.enums import ChannelType
import json
from discord.ext import commands

#if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    #discord.opus.load_opus('opus')
    #print("Loaded opus!")
discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')

client = discord.Client()

voice_clients = {}
voice_channels = {}
clients = []

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    channels = client.get_all_channels()
    for channel in channels:
        if channel.type == ChannelType.voice:
            if channel.name == 'Rust':
                voice_clients[channel.server.name] = await client.join_voice_channel(channel)
                voice_channels[channel.server.name] = channel


class SimpleServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        clients.append(self)

    def data_received(self, data):
        print("data_received: {}".format(data.decode()))
        j = json.loads(data.decode())
        #if j['secret_key'] == 'ife923f9aj9vfj3020':
        if j['secret_key'] == '123zxc':
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
                   player = vc.create_ffmpeg_player(full_path)
                   player.start()
        
    def connection_lost(self, ex):
        clients.remove(self)


coro = client.loop.create_server(SimpleServer, port=1234)
server = client.loop.run_until_complete(coro)

for socket in server.sockets:
    print("serving on {}".format(socket.getsockname()))

client.run('MzY2MDAxNTg3MTY1ODU1NzU0.DLmhFw.0v3pvdGPd29zRoehFhzJ46OO6TA')

