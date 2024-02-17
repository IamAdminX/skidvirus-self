import datetime
import os
import time

import requests
from colorama import Fore


os.system('cls')

def change_vanity(code: str, server_id: str, token: str) -> bool:
    response = requests.patch(
        f"https://discord.com/api/v9/guilds/{server_id}/vanity-url",
        headers={"authorization": token},
        json={"code": code},
    )
    if response.ok:
        print(f"{Fore.BLUE} <*> Updated invite successfully, your server can now be accessed by 'discord.gg/{code}'. ")
        return True
    else:
        print(f"{Fore.RED} <!> Failed to update vanity url. Status code: {response.status_code}")
        return False


def check_vanity(code: str) -> bool:
    response = requests.get(f"https://discord.com/api/v9/invites/{code}")
    if response.status_code == 404:
        return True
    else:
        print(f"\n{Fore.RED} <!> Vanity is still in use.")
        return False


def snipe() -> None:
    token = input(f"{Fore.RED} <~> Token: {Fore.BLUE}")
    code = input(f"{Fore.RED} <~> Vanity code to snipe: {Fore.BLUE}")
    server_id = input(f"{Fore.RED} <~> Guild ID: {Fore.BLUE}")
    delay = int(input(f"{Fore.RED} <~> Delay between checks (seconds): {Fore.BLUE}"))

    try:
        while not check_vanity(code):
            time.sleep(delay)
            cur_time = datetime.datetime.now().strftime("%X")
            print(f"{Fore.BLUE} <*> Last checked at {cur_time} ", end="", flush=True)

        change_vanity(code, server_id, token)

    except KeyboardInterrupt:
        pass