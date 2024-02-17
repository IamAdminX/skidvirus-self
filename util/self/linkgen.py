import ctypes
import os
import random
import string
import time

import requests
from colorama import Fore

from util.plugins.common import *


class ServerLinkGen:
    def main(self):
        num = int(input(f"{Fore.RED} <~> Number of generations: {Fore.BLUE}"))
        webhookk = input(f'{Fore.RED} <~> Webhook Url: {Fore.BLUE}')
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        valid = []
        invalid = 0

        for i in range(num):
            try:
                code = "".join(random.choices(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase,
                    k=7
                ))
                url = f"https://discord.gg/{code}"

                result = self.quickChecker(url, webhookk)

                if result:
                    valid.append(url)
                else:
                    invalid += 1
            except Exception as e:
                print(f" <!> Error: {url}")

            if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Server Link Generator and Checker - {len(valid)} Valid | {invalid} Invalid - Made by Xvirus™"
                )
                print("")

        print(f"""
        Results:
        Valid: {len(valid)}
        Invalid: {invalid}
        Valid Server Links: {', '.join(valid)}
        """)

        

    def generator(self, amount):
        print(" <!> Wait, Generating for you")

        start = time.time()

        for i in range(amount):
            code = "".join(random.choices(
                string.ascii_uppercase + string.digits + string.ascii_lowercase,
                k=7
            ))

            url = f"https://discord.gg/{code}"
            print(url)

        print(f" <!> Genned {amount} server links | Time taken: {round(time.time() - start, 5)}s\n")

    def fileChecker(self, notify=None):
        valid = []
        invalid = 0

        for line in valid:
            server_link = line.strip("\n")

            url = f"https://discord.com/api/v9/invites/{server_link}"

            response = requests.get(url)

            if response.status_code == 200:
                print(f"{Fore.BLUE} <*> Valid:{Fore.GREEN} {server_link}")
                valid.append(server_link)

                if notify is not None:
                    self.send_webhook(notify, server_link)
                else:
                    break
            else:
                print(f"{Fore.BLUE} <!> Invalid:{Fore.RED} {server_link}")
                invalid += 1

        return {"valid": valid, "invalid": invalid}

    def quickChecker(self, server_link, notify=None):
        url = f"https://discord.com/api/v9/invites/{server_link}"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"{Fore.BLUE} <*> Valid:{Fore.GREEN} {server_link}", flush=True, end="" if os.name == 'nt' else "\n")

            if notify is not None:
                self.send_webhook(notify, server_link)

            return True
        else:
            print(f"{Fore.BLUE} <!> Invalid:{Fore.RED} {server_link}", flush=True, end="" if os.name == 'nt' else "\n")
            return False

    def send_webhook(self, webhook_url, server_link):
        data = {
            "content": f"@everyone | A valid server link has been found => {server_link}"
        }
        requests.post(webhook_url, json=data)


def serverlinkgen():
    SetTitle("Generating Server Links")
    Gen = ServerLinkGen()
    Gen.main()
