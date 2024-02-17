import os
import requests
from time import sleep
from colorama import Fore
import threading
from util.plugins.common import *

def RuleAccepter(guild_id, token):
    headers = {
        "Authorization": token
    }
    get_rules = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false", proxies={"http": f'{proxy()}'}, headers=headers).json()
    response = requests.put(f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me", proxies={"http": f'{proxy()}'}, headers=headers, json=get_rules)
    if response.status_code == 201:
        print(f"{Fore.BLUE} <*> Successfully Accepted Rules {Fore.RED}({response.status_code})")
    if response.status_code == 410:
        print(f"{Fore.RED} <!> Rules Are Already Accepted {Fore.BLUE}({response.status_code})")
    else:
        print(f"{Fore.RED} <!> Error Accepting Rules {Fore.BLUE}({response.status_code})")

def AcceptRules():
    SetTitle("Rule Accepter")
    guild_id = input(f"{Fore.RED} <~> Guild ID: {Fore.BLUE}")
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_tokens")

    if not os.path.exists(temp_folder):
        print(f"{Fore.RED} <!> No Tokens Were Found In The Cache")
        sleep(2)
        __import__("Xvirus").main1()
    else:
        with open(temp_folder, "r") as f:
            tokens = f.read().strip().splitlines()

        tokens = [token for token in tokens if token.strip()]

        if not tokens:
            print(f"{Fore.RED} <!> No Tokens Were Found In The Cache")
            sleep(2)
            __import__("Xvirus").main1()
        else:
            threads = []
            for token in tokens:
                thread = threading.Thread(target=RuleAccepter, args=(guild_id, token))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()