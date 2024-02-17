import concurrent.futures
import random
import string
from dataclasses import dataclass
import os
import tls_client
from colorama import Fore
import time
import requests

@dataclass
class NickData:
    pass

@dataclass
class Instance(NickData):
    client: tls_client.sessions
    token: str
    nick: str
    headers: dict
    guild_id: str

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

class NickToken:
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
        self.session.headers.update({"Authorization":self.instance.token})
        result=self.session.patch(f"https://discord.com/api/v9/guilds/{self.instance.guild_id}/members/@me",json={
            'session_id': self.rand_str(32),
            'nick': self.instance.nick
        })

        if result.status_code == 200:
            print(f" {Fore.BLUE}<*> Successfully Changed NickName To {self.instance.nick} {Fore.RED}({str(result.status_code)})")
        elif result.text.startswith('{"captcha_key"'):
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
        elif result.text.startswith('{"message": "401: Unauthorized'):
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
        elif "Cloudflare" in result.text:
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
        elif "\"code\": 40007" in result.text:
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (User Banned)")
        elif "\"code\": 40002" in result.text:
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
        elif "\"code\": 10006" in result.text:
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Invalid Invite)")
        else:
            print(f" {Fore.RED}<!> Error Changing NickName To {self.instance.nick} {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")

class intilize:
    def start(i):
        NickToken(i).send()

def ServerNicker():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_tokens")

    if not os.path.exists(temp_folder):
        return []

    with open(temp_folder, "r") as f:
        tokens = f.read().strip().splitlines()

    tokens = [token for token in tokens if token.strip()]

    if not tokens:
        print(f" {Fore.RED}<!> No Tokens Were Found In The Cache")
        time.sleep(2)
        __import__("Xvirus").main1()

    instances = []
    max_threads=5
    guild_id = input(f"{Fore.RED} <~> Guild ID: {Fore.BLUE}")
    nick = input(f"{Fore.RED} <~> Nick Name: {Fore.BLUE}")

    for i in range(len(tokens)):
        header = headers
        instances.append(Instance(
            client=tls_client.Session(
            client_identifier=f"chrome_{random.randint(110,116)}",
            random_tls_extension_order=True
        ),
            token=tokens[i],
            headers=header,
            nick=nick,
            guild_id=guild_id
        ))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for i in instances:
            executor.submit(intilize.start, i)