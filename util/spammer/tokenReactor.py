import os
import re
import random
import requests
import time
import threading
from colorama import Fore
from functools import partial
from itertools import cycle
import tls_client


def get_tokens():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_tokens")

    if not os.path.exists(temp_folder):
        return []

    with open(temp_folder, "r") as f:
        tokens = f.read().strip().splitlines()

    tokens = [token for token in tokens if token.strip()]

    if not tokens:
        print(f"{Fore.RED} <!> No Tokens Were Found In The Cache")

    return tokens
    
def get_message(token, channel_id, message_id):
    session = tls_client.sessions
    headers = {"Authorization": token}
    try:
        message = session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1&around={message_id}", headers=headers).json()
        return message[0]
    except Exception as e:
        return {"code": 10008}

def get_message_info(msg_link = None):
        if msg_link is None:
            msg_link = input(f"{Fore.RED} <~> Message Link: {Fore.BLUE}")
        rg = re.compile(r"^https:\/\/(ptb.|canary.|)discord.com\/channels\/\d+\/\d+\/\d+$")
        if rg.match(msg_link):
            guild_id = msg_link.split("/")[4]
            channel_id = msg_link.split("/")[5]
            message_id = msg_link.split("/")[6]
            return {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "message_id": message_id,
            }
        else:
            print(f"{Fore.RED} <!> Invalid Message")
            return None
            
def get_message_reactions(channel_id, message_id, iteration=0):
    try:
        if iteration > 5:
            return None
        message = get_message(
            token=random.choice(get_tokens()),
            channel_id=channel_id,
            message_id=message_id
        )

        if message.get("code") == 10008:
            return get_message_reactions(channel_id, message_id, iteration=iteration+1)
        emojis = []
        if len(message["reactions"]) == 0:
            return None
        for reaction in message["reactions"]:
            emoji = reaction["emoji"]
            if emoji["id"] == None:
                emojis.append({
                    "name": emoji["name"],
                    "count": reaction["count"],
                    "custom": False
                })
            else:
                emojis.append({
                    "name": f"{emoji['name']}:{emoji['id']}",
                    "count": reaction["count"],
                    "custom": True
                })

        return emojis
    except Exception as e:
        print(e)
        return None
            
def react(emoji, message_id, channel_id, token = None,):
    client = tls_client.Session(
            client_identifier=f"chrome_{random.randint(110, 116)}",
            random_tls_extension_order=True
        )
    headers = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'sv-SE',
        'x-discord-timezone': 'Europe/Stockholm',
        'Authorization': token
    }

    result = session.put(
        f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me?location=Message&burst=false",
        headers=headers
    )

    if result.status_code == 200:
        print(f" {Fore.BLUE}<*> Successfully Pressing Button {Fore.RED}({str(result.status_code)})")
    elif result.text.startswith('{"captcha_key"'):
        print(f" {Fore.RED}<!> Error Pressing Button {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
    elif "Cloudflare to restrict access</title>" in result.text:
        print(f" {Fore.RED}<!> Error Pressing Button {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
    else:
        print(f" {Fore.RED}<!> Error Pressing Button {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")

def reactor():
    msg = get_message_info()
    if msg is None:
        print(f"{Fore.RED}ERROR: {Fore.LIGHTWHITE_EX}Invalid message link")
        time.sleep(3)
        return

    channel_id = msg["channel_id"]
    message_id = msg["message_id"]

    emojis = get_message_reactions(channel_id, message_id)
    if emojis is None:
        print(f"{Fore.RED}Invalid message id")
        return

    for num, emoji in enumerate(emojis):
        print(f"{Fore.RED} <*> {Fore.BLUE}({num}) {Fore.RED}Emoji: {Fore.BLUE}{emoji['name'].replace(' ', '')} {'[CUSTOM]' if emoji['custom'] else ''}   {Fore.BLUE}Reaction count: {Fore.BLUE}{emoji['count']}")

    emojinum = input("emoji number")
    for emoji in emojis:
        if emojis.index(emoji) == int(emojinum):
            emoji = emoji['name'].replace(" ", "")
            break

    num_threads = 10
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=react, args=(emoji, message_id, channel_id))
        thread.start()
        threads.append(thread)