import os
from json import dumps, loads
from time import sleep
import threading

from colorama import Fore
from websocket import WebSocket

def get_token_list():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_tokens")

    if not os.path.exists(temp_folder):
        return []

    with open(temp_folder, "r") as f:
        tokens = f.read().strip().splitlines()

    tokens = [token for token in tokens if token.strip()]

    if not tokens:
        print(f" {Fore.RED}<!> No Tokens Were Found In The Cache")
        sleep(2)

    return tokens

def vcjoiner():
    server = int(input(f' {Fore.RED}<~> Guild ID:{Fore.BLUE} '))
    channel = int(input(f' {Fore.RED}<~> Voice Channel ID:{Fore.BLUE} '))
    deaf = input(f' {Fore.RED}<~> Defean: {Fore.BLUE}(y/n)? ')
    if deaf == 'y':
        deaf = True
    else:
        deaf = False
    mute = input(f' {Fore.RED}<~> Mute: {Fore.BLUE}(y/n)? ')
    if mute == 'y':
        mute = True
    else:
        mute = False
    video = input(f' {Fore.RED}<~> Video Cam: {Fore.BLUE}(y/n)? ')
    if video == 'y':
        video = True
    else:
        video = False
    
    def run(token = None):
        ws = WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=8&encoding=json')
        hello = loads(ws.recv())
        heartbeat_interval = hello['d']['heartbeat_interval']
        ws.send(dumps({
            'op': 2,
            'd': {
                'token': token,
                'properties': {
                    '$os': 'windows',
                    '$browser': 'Discord',
                    '$device': 'desktop' } } }))
        ws.send(dumps({
            'op': 4,
            'd': {
                'guild_id': server,
                'channel_id': channel,
                'self_mute': mute,
                'self_deaf': deaf,
                'self_video': video } }))
        ws.send(dumps({
            'op': 18,
            'd': {
                'type': 'guild',
                'guild_id': server,
                'channel_id': channel,
                'preferred_region': 'singapore' } }))
        ws.send(dumps({
            'op': 1,
            'd': None }))
        sleep(0.1)
        
        response = loads(ws.recv())
        status_code = response.get('s')


    threads = []
    tokenlist = get_token_list()
    for token in tokenlist:
        thread = threading.Thread(target=run, args=(token,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    