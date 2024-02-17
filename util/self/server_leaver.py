import threading

import requests
from colorama import Fore

from util.plugins.common import *


def leave_guild(guild, token):
    try:
        response = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild["id"]}', headers=getheaders(token))
        if response.status_code == 204 or response.status_code == 200:
            print(f"{Fore.BLUE} <*> Left guild: {Fore.WHITE}" + guild['name'] + Fore.RESET + f"({response.status_code})")
        elif response.status_code == 400:
            requests.delete(f'https://discord.com/api/v9/guilds/{guild["id"]}', headers=getheaders(token))
            print(f'{Fore.RED} <*> Deleted guild: {Fore.WHITE}' + guild['name'] + Fore.RESET + f"({response.status_code})")
        else:
            print(f" {Fore.RED}<!> Error Joining Server {Fore.RED}({str(response.status_code)}){Fore.BLUE} ({response.text})")
    except Exception as e:
        print(f" {Fore.RED}<!> Error Joining Server {Fore.RED}({str(response.status_code)}){Fore.BLUE} ({response.text})")

def Leaver():
    SetTitle("Server Leaver")
    token = input(f'{Fore.RED} <~> Token: {Fore.BLUE}')
    CheckToken(token)
    if token.startswith("mfa."):
        print(f'{Fore.RED} <!> Just a heads-up, Xvirus won\'t be able to delete the servers since the account has 2FA enabled')

    guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", proxies={"http": f'{proxy()}'}, headers=getheaders(token)).json()

    threads = []
    for guild in guilds:
        thread = threading.Thread(target=leave_guild, args=(guild, token))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

