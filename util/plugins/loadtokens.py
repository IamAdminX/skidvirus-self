import asyncio
import os
import re
import threading
import webbrowser
from time import sleep
import aiohttp
from colorama import Fore
from util.plugins.common import *

XVIRUS_TOKENS_FILE = os.path.join(os.environ["TEMP"], "xvirus_tokens")
BATCH_SIZE = 50

async def check_tokens_batch(session, tokens, valid_tokens, invalid_tokens, locked_tokens):
    tasks = []
    for token in tokens:
        extracted_token = extract(token)
        task = check_token(session, extracted_token, valid_tokens, invalid_tokens, locked_tokens)
        tasks.append(task)
    await asyncio.gather(*tasks)

async def check_token(session, token, valid_tokens, invalid_tokens, locked_tokens):
    try:
        async with session.get('https://discord.com/api/v9/users/@me/relationships', headers=getheaders(token)) as response:
            if response.status == 200:
                valid_tokens.append(token)
                print(f"{Fore.GREEN} <*> Valid{Fore.BLUE} {token}{Fore.LIGHTBLACK_EX} ({response.status})")
            elif response.status == 401 or response.status == 403:
                locked_tokens.append(token)
                print(f"{Fore.LIGHTBLACK_EX} <~> Locked{Fore.BLUE} {token}{Fore.LIGHTBLACK_EX} ({response.status})")
            elif response.status == 404:
                invalid_tokens.append(token)
                print(f"{Fore.RED} <!> Invalid{Fore.BLUE} {token}{Fore.LIGHTBLACK_EX} ({response.status})")
            else:
                print(f"{Fore.LIGHTRED_EX} <!> Error{Fore.BLUE} {token}{Fore.LIGHTBLACK_EX} ({response.status})")
    except Exception as e:
        locked_tokens.append(token)
        print(f"{Fore.LIGHTBLACK_EX} <!> Locked{Fore.BLUE} {token}{Fore.LIGHTBLACK_EX} (Error: {e})")

def threaded_checker(tokens, valid_tokens, invalid_tokens, locked_tokens):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def token_checker():
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=5)) as session:
            for i in range(0, len(tokens), BATCH_SIZE):
                batch = tokens[i:i + BATCH_SIZE]
                extracted_batch = [extract(token) for token in batch]
                await check_tokens_batch(session, extracted_batch, valid_tokens, invalid_tokens, locked_tokens)

    loop.run_until_complete(token_checker())

def token_checker_threaded(tokens):
    valid_tokens = []
    invalid_tokens = []
    locked_tokens = []

    threads = []
    num_threads = len(tokens) // BATCH_SIZE + 1

    for i in range(num_threads):
        start_idx = i * BATCH_SIZE
        end_idx = (i + 1) * BATCH_SIZE
        thread_tokens = tokens[start_idx:end_idx]
        t = threading.Thread(target=threaded_checker, args=(thread_tokens, valid_tokens, invalid_tokens, locked_tokens))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return valid_tokens, invalid_tokens, locked_tokens

def save_valid_tokens(valid_tokens, write_locked_tokens=False, locked_tokens=None):
    with open(XVIRUS_TOKENS_FILE, 'w') as f:
        for token in valid_tokens:
            f.write(token + "\n")

    if write_locked_tokens and locked_tokens:
        with open(XVIRUS_TOKENS_FILE, 'a') as f:
            for token in locked_tokens:
                f.write(token + "\n")

def load_tokens():
    if os.path.exists(XVIRUS_TOKENS_FILE):
        with open(XVIRUS_TOKENS_FILE, 'r') as f:
            return [line.strip() for line in f.readlines()]
    else:
        print(" <!> No valid tokens found in the cache.")
        return []

def verify_written_tokens(valid_tokens):
    written_tokens = load_tokens()
    return set(valid_tokens) == set(written_tokens)

def empty_tokens_file():
    with open(XVIRUS_TOKENS_FILE, 'w') as f:
        pass

def buyTokensDazeer(): 
    redirect = input(f"{Fore.RED} <~> Do you want to redirect to https://dazeer.mysellix.io/ (y/n): {Fore.BLUE}")
    if redirect.lower() == 'y':
        webbrowser.open("https://dazeer.mysellix.io/product/634d684f745af")
    elif redirect.lower() == 'n':
        print(" <!> Redirect not requested.")
    else:
        print(" <!> Invalid input. Redirect not requested.")

def buyTokensBody(): 
    redirect = input(f"{Fore.RED} <~> Do you want to redirect to https://bodyx.mysellix.io/product/ (y/n): {Fore.BLUE}")
    if redirect.lower() == 'y':
        webbrowser.open("https://bodyx.mysellix.io/product/64e4b3244c004")
    elif redirect.lower() == 'n':
        print(" <!> Redirect not requested.")
    else:
        print(" <!> Invalid input. Redirect not requested.")

def load_or_empty_tokens():
    tokens = []
    global tokens_emptied
    print(f'''
        {Fore.BLUE}[{Fore.RED}1{Fore.BLUE}] Save Tokens
        {Fore.BLUE}[{Fore.RED}2{Fore.BLUE}] Empty Tokens
        {Fore.BLUE}[{Fore.RED}3{Fore.BLUE}] Buy Tokens
    ''')
    choice = input(f'{Fore.RED} <~> Choice: {Fore.BLUE}').strip().lower()
    if choice == '1':
        path = input(f" {Fore.RED}<~> Enter the path to the tokens file: {Fore.BLUE}")

        if not os.path.exists(path):
            print(f" File '{path}' doesn't exist.")
            return

        with open(path, 'r') as f:
            tokens += [line.strip() for line in f.readlines()]

        valid_tokens, _, _ = token_checker_threaded(tokens)

        print("\n")
        print(f" {Fore.GREEN}<*> Valid: {len(valid_tokens)}")

        if valid_tokens:
            save_valid_tokens(valid_tokens)
            print(f" {Fore.BLUE} <*> Saved Valid Tokens To Cache.")
    elif choice == '2':
        empty_tokens_file()
        tokens_emptied = True
        print(f" {Fore.BLUE}<*> Xvirus Tokens Emptied.")
        return []
    elif choice == '3':
        buyTokensBody()
    else:
        print(f" {Fore.RED}<!> Invalid choice. No action taken.")

    return tokens if 'tokens' in locals() else []

def savetokens():
    global tokens_emptied
    tokens_emptied = False
    SetTitle("Token Management")
    load_or_empty_tokens()
