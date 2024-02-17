import base64
import datetime
import time
from concurrent.futures import ThreadPoolExecutor

from colorama import Fore

from util import *

def send(token, message, channelid, massping, amount=None):
    
    try:
        session, headers, cookie = Header.get_client(token)
        while True:
            try:
                if massping == 'y':
                    content = f"{message} {get_random_id(int(amount))} {rand_str(9)}"
                else:
                    content = message

                data = {'session_id': rand_str(32), "content": content}
                result = session.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers, cookies=cookie, json=data)

                if result.status_code == 200:
                    print(f" {Fore.BLUE}<*> Successfully Sent Message! [{message[:45]}...] {Fore.RED}({str(result.status_code)})")
                elif result.text.startswith('{"captcha_key"'):
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Captcha)")
                elif result.text.startswith('{"message": "401: Unauthorized'):
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Unauthorized)")
                elif "Cloudflare" in result.text:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (CloudFlare Blocked)")
                elif "\"code\": 40007" in result.text:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (User Banned)")
                elif "\"code\": 40002" in result.text:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Locked Token)")
                elif "\"code\": 10006" in result.text:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Invalid Invite)")
                elif "\"code\": 50013" in result.text:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (No Access)")
                elif "\"code\": 50001" in result.text:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (No Access)")
                elif result.status_code == 429:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.BLUE}({str(result.status_code)}){Fore.RED} (Rate Limit)")
                else:
                    print(f" {Fore.RED}<!> Error Sending Message! [{message[:45]}...] {Fore.RED}({str(result.status_code)}){Fore.BLUE} ({result.text})")
            except Exception as e:
                print(f"{e}")
    except Exception as e:
        print(f"{e}")

def raider():
    args = []
    tokens = get_tokens()

    if tokens is None:
        print(f" {Fore.RED}<!> Token retrieval failed or returned None.")
        return

    channel_id = input(f"{Fore.RED} <~> Channel ID: {Fore.BLUE}")
    message = input(f"{Fore.RED} <~> Message: {Fore.BLUE}")
    max_threads = input(f"{Fore.RED} <~> Thread Count: {Fore.BLUE}")
    massping = input(f"{Fore.RED} <~> Massping (y/n): {Fore.BLUE}")
    amount = None
    
    if massping == 'y':
        id_scraper()
        ids = get_ids()
        amount = input(f"{Fore.RED} <~> Amount Of pings (Don't exceed {len(ids)}): ")
    
    try:
        if not max_threads.strip():
            max_threads = "13"
        else:
            max_threads = int(max_threads)
    except ValueError:
        max_threads = "13"

    while True:
        if tokens:
            def thread_send(token):
                try:
                    token = extract(token)
                    args = [token, message, channel_id, massping, amount]
                    send(*args)
                except Exception as e:
                    print(f"{e}")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=thread_send, args=(token,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
        else:
            print(f" {Fore.RED}<!> No tokens were found in cache")