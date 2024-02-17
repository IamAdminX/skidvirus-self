import re
import os
import requests
import time
import binascii
from decimal import Decimal
from colorama import Fore
import threading
import random
import tls_client


def get_message(token, channel_id, message_id):
    headers = {"Authorization": token}
    session = tls_client.sessions
    try:
        message = session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1&around={message_id}", headers=headers).json()
        return message[0]
    except Exception as e:
        return {"code": 10008}

def get_message_buttons(token, guild_id, channel_id, message_id):
    headers = {"Authorization": token}
    try:
        message = get_message(
            token=token,
            channel_id=str(channel_id),
            message_id=str(message_id),
        )
        if message.get("code") == 10008:
            return None
        buttons = []
        if len(message["components"]) == 0:
            return None
        for component in message["components"]:
            for button in component["components"]:
                buttons.append({
                    "label": button.get("label"),
                    "custom_id": button["custom_id"],
                    "application_id": message["author"]["id"],
                })

        return buttons
    except Exception as e:
        print(e)
        return None

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

def press(guild_id, channel_id, message_id, custom_id, application_id, amount = 999999999, token = None, flags = 0):
        try:
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
                'x-super-properties': 'eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTYuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNi4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmVfY3VycmVudCI6Imdvb2dsZSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
                'Authorization': token
            }

            payload = {
                "application_id": str(application_id),
                "channel_id": str(channel_id),
                "data": {
                    "component_type": 2,
                    "custom_id": str(custom_id)
                },
                "guild_id": str(guild_id),
                "message_flags": flags,
                "message_id": str(message_id),
                "nonce": str(Decimal(time.time() * 1000 - 1420070400000) * 4194304).split(".")[0],
                "session_id": str(binascii.b2a_hex(os.urandom(16)).decode('utf-8')),
                "type": 3,
            }

            session = tls_client.sessions
            headers.update({"content-type": "application/json"})
            headers.update({"referer": f"https://discord.com/channels/{guild_id}/{channel_id}"})
            for i in range(amount):
                result = session.post(f"https://discord.com/api/v9/interactions", headers=headers, json=payload)
                if result.status_code == 200:
                    print(f" {Fore.BLUE}<*> Successfully Pressing Button {Fore.RED}({str(result.status_code)})")
                elif result.text.startswith('{"captcha_key"'):
                    print(f" {Fore.RED}<!> Error Pressing Button {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
                elif result.text.startswith('{"message": "401: Unauthorized'):
                    print(f" {Fore.RED}<!> Error Pressing Button {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
                elif "Cloudflare to restrict access</title>" in result.text:
                    print(f" {Fore.RED}<!> Error Pressing Button {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
                else:
                    print(f" {Fore.RED}<!> Error Pressing Button {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")


        except Exception as e:
            print(f"{Fore.RED} <!> {e[:69]}")
            
            
def buttonPresser():
        message = get_message_info()
        if message is None:
            return None
        guild_id = message["guild_id"]
        channel_id = message["channel_id"]
        message_id = message["message_id"]

        buttons = get_message_buttons(
            token=random.choice(get_tokens()),
            guild_id=guild_id,
            channel_id=channel_id,
            message_id=message_id
        )
        
        if buttons == None:
            print(f"{Fore.RED} <!> Invalid message id (or message has no buttons)")
            return None

        for num, button in enumerate(buttons):
            print(f"{Fore.RED} <*> {Fore.BLUE}({num}) {Fore.RED}Button label: {Fore.BLUE}{button['label'].replace(' ', '') if button['label'] != None else 'None'}")

        buttonum = input(f"{Fore.RED} <~> Button Number: {Fore.BLUE}")
        for button in buttons:
            if buttons.index(button)==int(buttonum):
                custom_id = button['custom_id']
                application_id = button['application_id']
                break
                
        amount = input(f"{Fore.RED} <~> Amount (leave blank for infinite): {Fore.BLUE}")
        if amount == "":
            amount = 999999999
            
        elif not amount.isdigit():
            print(f"{Fore.RED} <!> Invalid input using defult amount")
            amount = 999999999
        
        amount = int(amount)
        
        num_threads = 10
        threads = []

        for _ in range(num_threads):
            thread = threading.Thread(target=press, args=(guild_id, channel_id, message_id, custom_id, application_id, amount))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()