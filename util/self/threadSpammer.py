import os
import requests
from time import sleep
from colorama import Fore
import threading
from util.plugins.common import *

def make_thread(channel_id, message, title, token):
    headers = {
        "Authorization": token,
        "content-type": "application/json"
    }

    req = requests.post(
        f"https://discord.com/api/v9/channels/{channel_id}/threads",
        proxies={"http": f'{proxy()}'},
        headers=headers,
        json={
            "auto_archive_duration": 1440,
            "name": title,
            "type": 11
        }
    )
    if req.status_code == 201:
        thread_id = req.json()["id"]
        req1 = requests.post(
            f"https://discord.com/api/v9/channels/{thread_id}/messages",
            proxies={"http": f'{proxy()}'},
            headers=headers,
            json={
                "content": message,
                "tts": False
            }
        )

        if req1.status_code == 200:
            print(f" {Fore.BLUE}<*> Successfully Created Thread {Fore.RED}({response.status_code})")
        else:
            print(f" {Fore.RED}<!> Error Creating Thread {Fore.BLUE}({response.status_code})")

def threadSpammer():
    channel_id = input(f"{Fore.RED} <~> Channel ID: {Fore.BLUE}")
    message = input(f"{Fore.RED} <~> Message: {Fore.BLUE}")
    title = input(f"{Fore.RED} <~> Thread Title: {Fore.BLUE}")
    
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_tokens")

    if not os.path.exists(temp_folder):
        print(f" {Fore.RED}<!> No Tokens Were Found In The Cache")
        sleep(2)
        exit()

    with open(temp_folder, "r") as f:
        tokens = f.read().strip().splitlines()

    tokens = [token for token in tokens if token.strip()]

    if not tokens:
        print(f" {Fore.RED}<!> No Tokens Were Found In The Cache")
        sleep(2)
        exit()
    else:
        threads = []
        for token in tokens:
            thread = threading.Thread(target=make_thread, args=(channel_id, message, title, token))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()