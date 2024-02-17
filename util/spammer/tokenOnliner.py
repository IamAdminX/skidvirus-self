import os
import json
import threading
import time
import random
import sys
import websocket
from colorama import Fore

def onliner():
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

    class Onliner:
        def __init__(self, token) -> None:
            self.token    = token
            self.statuses = ["online", "idle", "dnd"]

        def __online__(self):
            ws = websocket.WebSocket()
            ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
            response = ws.recv()
            event = json.loads(response)
            heartbeat_interval = int(event["d"]["heartbeat_interval"]) / 1000
            ws.send(
                json.dumps(
                    {
                        "op": 2,
                        "d": {
                            "token": self.token,
                            "properties": {
                                "$os": sys.platform,
                                "$browser": "RTB",
                                "$device": f"{sys.platform} Device",
                            },
                            "presence": {
                                "status": random.choice(self.statuses),
                                "since": 0,
                                "activities": [],
                                "afk": False,
                            },
                        },
                        "s": None,
                        "t": None,
                    }
                )
            )
            if len(self.token) > 55:
                truncated_content = self.token[:55]
            else:
                truncated_content = self.token
            print(f"{Fore.RED} <*> Successfully Onlined {Fore.BLUE}({truncated_content}{Fore.RED}...{Fore.BLUE})")

            while True:
                heartbeatJSON = {
                    "op": 1, 
                    "token": self.token, 
                    "d": "null"
                }
                ws.send(json.dumps(heartbeatJSON))
                time.sleep(heartbeat_interval)

    threads = []
    for token in tokens:
        thread = threading.Thread(target=Onliner(token).__online__)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
