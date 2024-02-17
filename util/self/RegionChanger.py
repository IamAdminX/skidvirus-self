import requests
import time
from colorama import Fore

regions = {
    'brazil',
    'hongkong',
    'india',
    'japan',
    'rotterdam',
    'russia',
    'singapore',
    'south-korea',
    'southafrica',
    'sydney',
    'us-central',
    'us-east',
    'us-south',
    'us-west'
}

def change(token, chnid):
    headers = {
        'Authorization': token,
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
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlW2JvdLjM3OS42Mi4yMDZfcmRlcF93ZWJfc2Vydml2YWxfYnV5Il0vNTM3LjM2IChLSFRTLCBsaWtlIEdlY2tvKSBEaXNjb3JkLzEuMC.451418a0f0d94361f59883e1a93c6742',
    }

    while True:
        for region in regions:
            data = {"region": region}
            result = requests.patch(f"https://discord.com/api/v9/channels/{chnid}/call", headers=headers, json=data)
            if result.status_code == 204:
                print(f" {Fore.BLUE}<*> Successfully Changed Region to [{region}] {Fore.RED}({str(result.status_code)})")
            elif result.text.startswith('rate limited'):
                print(f" {Fore.BLUE}<*> Successfully Rate Limited! {Fore.RED}({str(result.status_code)})")
            elif result.text.startswith('{"captcha_key"'):
                print(f" {Fore.RED}<!> Error Changing Region to [{region}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
            elif result.text.startswith('{"message": "401: Unauthorized'):
                print(f" {Fore.RED}<!> Error Changing Region to [{region}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
            elif "Cloudflare" in result.text:
                print(f" {Fore.RED}<!> Error Changing Region to [{region}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
            elif "\"code\": 40002" in result.text:
                print(f" {Fore.RED}<!> Error Changing Region to [{region}] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
            else:
                print(f" {Fore.RED}<!> Error Changing Region to [{region}] {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")
            time.sleep(0.5)

def regionChanger():
    token = input(f"{Fore.RED} <~> Token: {Fore.BLUE}")
    chnid = input(f"{Fore.RED} <~> Channel ID: {Fore.BLUE}")
    change(token, chnid)