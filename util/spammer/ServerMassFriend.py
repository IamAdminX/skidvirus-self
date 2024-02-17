import concurrent.futures
import os
import random
import string
import time
from dataclasses import dataclass
from time import sleep

import requests
import tls_client
from colorama import Fore
from util import *

@dataclass
class FrienderData:
    pass

@dataclass
class Instance(FrienderData):
    client: tls_client.sessions
    token: str
    user: str
    headers: dict

headers = {
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'sv,sv-SE;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'referer': 'https://discord.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'sv-SE',
    'x-discord-timezone': 'Europe/Stockholm',
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTYgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTg2MDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM1MjM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
}

class Friender:
    def __init__(self, data:Instance) -> None:
        self.session = data.client
        self.session.headers = data.headers
        self.get_cookies()
        self.instance = data

    def rand_str(self, length:int) -> str:
        return ''.join(random.sample(string.ascii_lowercase+string.digits, length))

    def get_cookies(self) -> None:
        site = self.session.get("https://discord.com")
        self.session.cookies = site.cookies

    def send(self) -> None:
        self.session.headers.update({"Authorization": self.instance.token})
        result = self.session.post(f"https://discord.com/api/v9/users/@me/relationships", json={
            'session_id': self.rand_str(32),
            'username': self.instance.user
        })

        if result.status_code == 204:
            print(f" {Fore.BLUE}<*> Successfully Sent Friend Request To {self.instance.user} {Fore.RED}({str(result.status_code)})")
        elif result.text.startswith('{"captcha_key"'):
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
        elif result.text.startswith('{"message": "401: Unauthorized'):
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
        elif "Cloudflare" in result.text:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
        elif "\"code\": 40007" in result.text:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (User Banned)")
        elif "\"code\": 40002" in result.text:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
        elif "\"code\": 10006" in result.text:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Invalid Invite)")
        elif "\"code\": 80004" in result.text:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Old Username System)")
        elif "\"code\": 80000" in result.text:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Friend Requests Disabled)")
        else:
            print(f" {Fore.RED}<!> Error Sending Friend Request To {self.instance.user} {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")

class intilize:
    def start(i):
        Friender(i).send()
    
def reset_users():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_usernames")

    if os.path.exists(temp_folder):
        os.remove(temp_folder)

def scrapeUsername():
        reset_users()
        token = get_random_token()
        headers = {
            'Authorization':token,
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'sv,sv-SE;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'sv-SE',
            'x-discord-timezone': 'Europe/Stockholm',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTYgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTg2MDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM1MjM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        }
        temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_ids")
        with open(temp_folder, 'r') as userids_file:
            user_ids = userids_file.read().splitlines()
        user_id_to_username = {}
        for user_id in user_ids:
            result = requests.get(f"https://discord.com/api/v9/users/{user_id}", headers=headers)
            if result.status_code == 200:
                user_data = result.json()
                username = user_data.get('username', 'Username not found')
                user_id_to_username[user_id] = username
                print(f" {Fore.RED}<*> Successfully Converted {user_id} > {username} {Fore.BLUE}({str(result.status_code)})")
                temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_usernames")
                with open(temp_folder,"a", encoding='utf-8')as x:
                    x.write(f"{username}\n")
            elif result.text.startswith('{"captcha_key"'):
                print(f" {Fore.RED}<!> Error Getting Username {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
            elif result.text.startswith('{"message": "401: Unauthorized'):
                print(f" {Fore.RED}<!> Error Getting Username {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
            elif "Cloudflare" in result.text:
                print(f" {Fore.RED}<!> Error Getting Username {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
            elif "\"code\": 40002" in result.text:
                print(f" {Fore.RED}<!> Error Getting Username {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
            else:
                print(f" {Fore.RED}<!> Error Getting Username {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")

def ServerFriendReq():
    id_scraper()
    scrapeUsername()
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_usernames")

    if not os.path.exists(temp_folder):
        with open(temp_folder, 'w') as x:
            pass

    with open(temp_folder, "r") as f:
        usernames = f.read().strip().splitlines()

    usernames = [username for username in usernames if username.strip()]

    if not usernames:
        print(f" {Fore.RED}<!> No Usernames Were Found In The Cache")
        time.sleep(2)
        return

    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_tokens")

    if not os.path.exists(temp_folder):
        print(f" {Fore.RED}<!> No Tokens Were Found In The Cache")
        time.sleep(2)
        return

    while True:
        with open(temp_folder, "r") as f:
            tokens = f.read().strip().splitlines()

        tokens = [token for token in tokens if token.strip()]

        if not tokens:
            print(f" {Fore.RED}<!> No Tokens Were Found In The Cache")
            time.sleep(2)
            return

        max_threads = input(f"{Fore.RED} <~> Thread Count: {Fore.BLUE}")
        futures = []

        for token in tokens:
            if not usernames:
                break

            username = usernames.pop(0)
            header = headers
            instance = Instance(
                client=tls_client.Session(
                    client_identifier=f"chrome_{random.randint(110, 116)}",
                    random_tls_extension_order=True
                ),
                token=token,
                headers=header,
                user=username
            )
            futures.append(concurrent.futures.ThreadPoolExecutor(max_workers=1).submit(intilize.start, instance))

        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)