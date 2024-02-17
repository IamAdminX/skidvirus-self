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
    idd: str
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

class CreateDM:
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
        result=self.session.post(f"https://discord.com/api/v9/users/@me/channels",json={
            'session_id': self.rand_str(32),
            "recipients": [self.instance.idd],
        })

        if result.status_code == 200:
            print(f" {Fore.BLUE}<*> Successfully Created DM With [{self.instance.idd}] {Fore.RED}({str(result.status_code)})")
            if 'id' in result.json():
                channel_id = result.json()['id']
                self.send_message(channel_id) 
        elif result.text.startswith('{"captcha_key"'):
            print(f" {Fore.RED}<!> Error Creating DM [{self.instance.idd}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
        elif result.text.startswith('{"message": "401: Unauthorized'):
            print(f" {Fore.RED}<!> Error Creating DM [{self.instance.idd}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
        elif "Cloudflare" in result.text:
            print(f" {Fore.RED}<!> Error Creating DM [{self.instance.idd}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
        elif "\"code\": 40002" in result.text:
            print(f" {Fore.RED}<!> Error Creating DM [{self.instance.idd}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
        else:
            print(f" {Fore.RED}<!> Error Creating DM [{self.instance.idd}] {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")
    
    def send_message(self, channel_id) -> None:
        self.session.headers.update({"Authorization":self.instance.token})
        result=self.session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages",json={
            'session_id': self.rand_str(32),
            'content': self.instance.message
        })

        truncated_message = self.instance.message[:69]

        if result.status_code == 200:
            print(f" {Fore.BLUE}<*> Successfully Sent Message [{truncated_message}] In [{channel_id}] {Fore.RED}({str(result.status_code)})")
        elif result.text.startswith('{"captcha_key"'):
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
        elif result.text.startswith('{"message": "401: Unauthorized'):
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
        elif "Cloudflare" in result.text:
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
        elif "\"code\": 40002" in result.text:
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
        elif "\"code\": 50007" in result.text:
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Couldnt send message)")
        elif "\"code\": 50009" in result.text:
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (User Has Dms Disabled)")
        else:
            print(f" {Fore.RED}<!> Error Sending Message [{truncated_message}] In [{channel_id}] {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")

channel_ids = []

class intilize:
    def start(i):
        CreateDM(i).send()

def ServerMassDM():
    id_scraper()
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_ids")

    if not os.path.exists(temp_folder):
        with open(temp_folder, 'w') as x:
            pass

    with open(temp_folder, "r") as f:
        ids = f.read().strip().splitlines()

    ids = [idd for idd in ids if idd.strip()]

    if not ids:
        print(f" {Fore.RED}<!> No ids Were Found In The Cache")
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
        message = input(f"{Fore.RED} <~> Message: {Fore.BLUE}")
        futures = []

        for token in tokens:
            if not ids:
                break

            idd = ids.pop(0)
            header = headers
            instance = Instance(
                client=tls_client.Session(
                    client_identifier=f"chrome_{random.randint(110, 116)}",
                    random_tls_extension_order=True
                ),
                token=token,
                headers=header,
                idd=idd
            )
            futures.append(concurrent.futures.ThreadPoolExecutor(max_workers=1).submit(intilize.start, instance))

        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)