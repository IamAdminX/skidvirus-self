import base64
import ctypes
import getpass
import io
import json
import multiprocessing
import os
import os.path
import random
import re
import shutil
import socket
import string
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import types
import typing
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime
from distutils.version import LooseVersion
from time import sleep
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile

import colorama
import keyboard
import pkg_resources
import requests
import tls_client
import websocket
import wifi
from bs4 import BeautifulSoup
from colorama import Fore
from pystyle import Add, Anime, Center, Colorate, Colors, System, Write
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

THIS_VERSION = "1.7.5"
TARGET_VERSION = "114.0.1823.67"

def WebText():
    r = requests.get("https://cloud.xvirus.lol/webtext.txt")
    text = r.text.strip()
    print(f"{Fore.RED}Text Of The Week:\n {Fore.BLUE}{text}")
    sleep(2.5)

def CHANGE_LOG():
    print(f'''
    1. Improved all spammer options with better headers
    2. Added user mass dm
    3. Made the channel spammer so much faster
    4. Made the Id scraper faster and working (NOT Discum)
    5. Changed all the domains from xvirus.pro to xvirtus.lol
    6. Fixed some typos
    7. New choice visual
    8. Added proxy settings
    ''')

def VERSION_NOTES():
    print(f''' <!> IMPORTANT NOTES!

    1. Please dont change the name of the file cuz that will make conflicts with the code.
    2. When you wanna save your tokens make sure your txt file has every new token in a new line.
    3. https://github.com/kekeds/discord-joiner Was used to make the joiner
    4. You MUST run Xvirus as admin when updating
        ''')

def search_for_updates():
    clear()
    SetTitle("Checking For Updates")
    r = requests.get("https://pastebin.com/raw/LC3wx7D5")
    latest_version = r.text.strip()

    if latest_version != THIS_VERSION:
        SetTitle("New Xvirus Update Found!")
        print(f"""{Fore.RED}
            ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗  ██╗
            ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝  ██║
            ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗    ██║
            ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝    ╚═╝
            ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗  ██╗
            ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═╝
                {Fore.RED}Xvirus {THIS_VERSION} is outdated. Latest version is {latest_version}""")

        print(f"\n{Fore.RED} <~> Go to https://discord.gg/xvirustool to install the latest update")
        PETC()
        clear()

def restart():
        print_slow(f"{Fore.RED} <!> Restarting tool")
        sleep(2)
        subprocess.run("Xvirus-Tools.exe", shell=True)
        exit()

class Edge_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://msedgedriver.azureedge.net/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if TARGET_VERSION:
            self.target_version = TARGET_VERSION

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "edgedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_edgedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open("ms"+self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect


    def get_release_version_number(self):
        path = (
            "LATEST_STABLE"
            if not self.target_version
            else f"LATEST_RELEASE_{str(self.target_version).split('.', 1)[0]}"
        )
        urlretrieve(
            f"{self.__class__.DL_BASE}{path}",
            filename=f"{os.getenv('temp')}\\{path}",
        )
        with open(f"{os.getenv('temp')}\\{path}", "r+") as f:
            _file = f.read().strip("\n")
            content = ""
            for char in [x for x in _file]:
                for num in ("0","1","2","3","4","5","6","7","8","9","."):
                    if char == num:
                        content += char
        return LooseVersion(content)

    def fetch_edgedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        print(f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip")
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract("ms"+self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name
        
def get_driver():
    drivers = ["msedgedriver.exe"]

    print(f"\n{Fore.BLUE} <!> Checking Driver. . .")
    sleep(0.5)

    for driver in drivers:
        if os.path.exists(os.getcwd() + os.sep + driver):
            print(f" <!>{Fore.BLUE}{driver} already exists, continuing. . .{Fore.RESET}")
            sleep(0.5)
            return driver
    else:
        print(f"{Fore.RED} <!> Driver not found! Installing it for you")
        if os.path.exists(os.getenv('localappdata') + '\\Microsoft\\Edge'):
            Edge_Installer()
            print(f"{Fore.GREEN} <*> msedgedriver.exe Installed!{Fore.RESET}")
            return "msedgedriver.exe"
        else:
            print(f'<!> No compatible driver found. . . Proceeding with msedgedriver')
            Edge_Installer()
            print(f"{Fore.GREEN} <!> trying to install msedgedriver.exe{Fore.RESET}")
            return "msedgedriver.exe"
 
def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n'*120)
    return

def SetTitle(_str):
    system = os.name
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{_str} - Discord API Tools | https://xvirus.lol | Made By Xvirus™")
    elif system == 'posix':
        os.system(f"\033]0;{_str} - Discord API Tools | https://xvirus.lol | Made By Xvirus™\a", end='', flush=True)
    else:
        pass

def print_slow(_str):
    for letter in _str:
        sys.stdout.write(letter);sys.stdout.flush();sleep(0.04)

def print015(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.015)
    sys.stdout.write("\n")

def print01(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.015)

def CheckToken(token):
    url = 'https://discord.com/api/v9/users/@me'
    response = requests.get(url, headers=getheaders(token))
    if response.status_code == 200:
        print(f"{Fore.BLUE} <*> Valid Token{Fore.RED} ({response.status_code})")
    elif response.status_code == 401 or response.status_code == 403:
        print(f"{Fore.LIGHTBLACK_EX} <~> Locked Token{Fore.RED} ({response.status_code})")
    elif response.status_code == 404:
        print(f"{Fore.RED} <!> Invalid Token{Fore.BLUE} ({response.status_code})")
        sleep(1)
        __import__("Xvirus").main1()

def CheckWebhook(hook):
    try:
        response = requests.get(hook)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"\n{Fore.RED} <!> Invalid Webhook.")
        sleep(1)
        __import__("Xvirus").main1()

    try:
        json_data = response.json()
        j = json_data["name"]
        print(f"{Fore.BLUE} <*> Valid webhook! ({j})")
    except (KeyError, json.decoder.JSONDecodeError):
        print(f"\n{Fore.RED} <!> Invalid Webhook.")
        sleep(1)

def proxy_scrape():
    proxieslog = []
    SetTitle("Scraping Proxies")
    startTime = time.time()
    temp = os.getenv("temp")+"\\xvirus_proxies"
    Anime.Fade((logo), Colors.rainbow, Colorate.Vertical, time=5)

    def fetchProxies(url, custom_regex):
        global proxylist
        try:
            proxylist = requests.get(url, timeout=5).text
        except Exception:
            pass
        finally:
            proxylist = proxylist.replace('null', '')
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxieslog.append(f"{proxy[0]}:{proxy[1]}")

    proxysources = [
        ["http://spys.me/proxy.txt","%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",']
    ]
 
    threads = [] 
    for url in proxysources:
        t = threading.Thread(target=fetchProxies, args=(url[0], url[1]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    proxies = list(set(proxieslog))
    with open(temp, "w") as f:
        for proxy in proxies:
            for i in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")
    execution_time = (time.time() - startTime)
    print(f"{Fore.BLUE} <!> Done! Scraped{Fore.MAGENTA}{len(proxies): >5}{Fore.RED} in total => {Fore.RED}{temp} | {execution_time}ms")

def proxy():
    temp = os.getenv("temp") + "\\xvirus_proxies"

    if not os.path.isfile(temp) or os.stat(temp).st_size == 0:
        proxy_scrape()
    proxies = open(temp).read().split('\n')
    proxy = random.choice(proxies)

    return {'http': f'http://{proxy}', 'https': f'https://{proxy}'}

def get_proxies():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_proxies")
    
    with open(temp_folder, "w") as f:
        proxies = f.read().strip().splitlines()
    proxies = [proxy for proxy in proxies if proxy.strip()]
    return proxies

def clean_proxy(proxy):
        if isinstance(proxy, str):
            if '@' in proxy:
                return proxy
            elif len(proxy.split(':')) == 2:
                return proxy
            elif len(proxy.split(':')) == 4:
                return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
            else:
                if '.' in proxy.split(':')[0]:
                    return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
                else:
                    return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])
        elif isinstance(proxy, dict):
            if proxy.get("http://") or proxy.get("https://"):
                return proxy
            else:
                if proxy in [dict(), {}]:
                    return {}
                return {
                    "http://": proxy.get("http") or proxy.get("https"),
                    "https://": proxy.get("https") or proxy.get("http")
                }

def get_random_proxy():
        try:
            return random.choice(get_proxies())
        except:
            return {}

def get_proxy_type():
    h = "http"
    if "socks5" in h:
        h = "socks5"
    return h

heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }]

def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers

def check_wifi_connection():
    domains = ['https://www.google.com', 'https://www.facebook.com', 'https://www.apple.com']
    for domain in domains:
        try:
            urllib.request.urlopen(domain)
            return
        except urllib.error.URLError:
            pass

    while True:
        offline()
        for i in range(5, 0, -1):
            print(f"{Fore.RED}                                Retrying in {Fore.BLUE}{i} {Fore.RED}seconds", end='\r')
            time.sleep(1)
        clear()

def check_servers():
    domains = ['https://xvirus.lol', 'https://buy.xvirus.lol']
    online_count = 0
    fails = 0

    while fails < 2:
        for domain in domains:
            try:
                urllib.request.urlopen(domain)
                online_count += 1
                if online_count >= 1:
                    search_for_updates()
                    return
            except urllib.error.URLError:
                fails += 1

        for i in range(5, 0, -1):
            print(f"{Fore.RED}Xvirus Servers Are Offline At The Moment, Try Again Later.\n{Fore.RED} Retrying in {Fore.BLUE}{i} {Fore.RED}seconds", end='\r')
            time.sleep(1)
            clear()
        clear()

    if fails >= 2:
        print(f"{Fore.RED}Xvirus Cloud Is Unavailable Skipping Update Check!")
        time.sleep(2)
        clear()

def check_version():
        try:
            assert sys.version_info >= (3,7)
        except AssertionError:
            print(f"{Fore.RED} <!> Woopsie daisy, your Python version ({sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}) is not compatible with xvirus, please download Python 3.7+")
            sleep(5)
            print(" <!> exiting. . .")
            sleep(1.5)
            os._exit(0)

def get_username():
    temp_dir = tempfile.gettempdir()
    
    username_file = os.path.join(temp_dir, 'xvirus_username')

    if os.path.isfile(username_file):
        with open(username_file, 'r') as f:
            username = f.read().strip()
    else:
        clear()
        usernamelogo()
        username = input(f"""                            {Fore.BLUE}Your Username: """)
        
        with open(username_file, 'w') as f:
            f.write(username)
    
    return username

def setUsername(new: str):
    temp_dir = tempfile.gettempdir()
    username_file = os.path.join(temp_dir, 'xvirus_username')

    with open(username_file, 'w') as f:
        f.write(new)

def countTokens(print_count=False):
        temp_folder = tempfile.gettempdir()
        file_list = os.listdir(temp_folder)
        token_file = None

        for filename in file_list:
            if filename.startswith('xvirus_token'):
                token_file = os.path.join(temp_folder, filename)
                break

        if token_file is None:
            print(" <!> 'xvirus_token' file not found in the temp folder")
            return 0

        with open(token_file, 'r') as file:
            content = file.read()

        token_list = content.strip().split('\n')
        token_count = len(token_list)

        if print_count:
            print("Tokens:", token_count)

        return token_count

def extract(tokens):
    r = re.compile(r"(.+):(.+):(.+)")
    match = r.match(tokens)
    return match.group(3) if match else tokens

def get_pc_username(trigger=False):
    pcusername = getpass.getuser()
    if trigger:
        print("PC username:", pcusername)
    return pcusername

def count_proxies():
    temp = os.getenv("temp") + "\\xvirus_proxies"
    try:
        with open(temp, "r") as f:
            proxies = f.readlines()
        proxycount = len(proxies)
        return proxycount
    except FileNotFoundError:
        print(f"<!> xvirus_proxies file not found.")
        return 0

def WIP():
    SetTitle("This Option Is A WIP")
    input("This Option Is A Work In Progress, It Will Be Available In The Next Update!")

proxycount = count_proxies()
token_count = countTokens()
pc_username = get_pc_username(trigger=False)

def set_terminal_width(width):
    handle = ctypes.windll.kernel32.GetStdHandle(-11)

    new_size = ctypes.wintypes._COORD(width, ctypes.wintypes._COORD().Y)

    ctypes.windll.kernel32.SetConsoleScreenBufferSize(handle, new_size)
    ctypes.windll.kernel32.SetConsoleWindowInfo(handle, True, ctypes.byref(new_size))

xvirus_width = 120

def PETC():
    input(f'{Fore.RED}\n <~> Press ENTER to continue{Fore.RED}')

#######################################################################################################################

lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLACK_EX
r = Fore.RED

def getTheme():
    themes = ["xeme", "dark", "fire", "aqua", "neon", "rainbow"]
    with open(os.getenv("temp")+"\\xvirus_theme", 'r') as f:
        text = f.read()
        if not any(s in text for s in themes):
            print(f' <!> Invalid theme was given, Switching to default. . .')
            setTheme('xeme')
            sleep(2.5)
            __import__("Xvirus").main1()
        return text

def setTheme(new: str):
    with open(os.getenv("temp")+"\\xvirus_theme", 'w'): pass
    with open(os.getenv("temp")+"\\xvirus_theme", 'w') as f:
        f.write(new)

def main_banner1():
    if getTheme() == "xeme":
        banner1()
    elif getTheme() == "dark":
        banner1("dark")
    elif getTheme() == "fire":
        banner1("fire")
    elif getTheme() == "aqua":
        banner1("aqua")
    elif getTheme() == "neon":
        banner1("neon")
    elif getTheme() == "rainbow":
        banner1("rainbow")

def banner1(theme=None):
    if theme == "dark":
        print(Colorate.Vertical(Colors.black_to_white, (banner1Theme)))
    elif theme == "fire":
        print(Colorate.Vertical(Colors.red_to_yellow, (banner1Theme)))
    elif theme == "aqua":
        print(Colorate.Vertical(Colors.cyan_to_blue, (banner1Theme)))
    elif theme == "neon":
        print(Colorate.Vertical(Colors.blue_to_red, (banner1Theme)))
    elif theme == "rainbow":
        print(Colorate.Horizontal(Colors.rainbow, (banner1Theme)))
    else:
       print(f'''
{r}                                              <Xvirus Tools Self Options>
{r} ╔═══                              ═══╗ ╔═══                               ═══╗ ╔═══                               ═══╗
{r} ║   ({lb}01{r}) {lb}> Token Login               {r}║ ║   {r}({lb}10{r}) {lb}> Seizure                    {r}║ ║   {r}({lb}19{r}) {lb}> Webhook Tool{r}               ║
{r}     ({lb}02{r}) {lb}> Token Info                      {r}({lb}11{r}) {lb}> Leave And Delete Servers         {r}({lb}20{r}) {lb}> Webhook Generator{r}
{r}     ({lb}03{r}) {lb}> Token Disabler                  {r}({lb}12{r}) {lb}> Remove Friends                   {r}({lb}21{r}) {lb}> Nitro Generator{r}
{r}     ({lb}04{r}) {lb}> Token Brute-Force               {r}({lb}13{r}) {lb}> Block Friends                    {r}({lb}22{r}) {lb}> Server Link Generator{r}
{r}     ({lb}05{r}) {lb}> Token Vc Mass Region            {r}({lb}14{r}) {lb}> Dm @everyone                     {r}({lb}23{r}) {lb}> Server Nuker{r}
{r}     ({lb}06{r}) {lb}> Token Checker                   {r}({lb}15{r}) {lb}> Delete DMs                       {r}({lb}24{r}) {lb}> Group Spammer{r}
{r}     ({lb}07{r}) {lb}> Token Nuker                     {r}({lb}16{r}) {lb}> Clear DMs                        {r}({lb}25{r}) {lb}> SelfBot Spammer{r}
{r}     ({lb}08{r}) {lb}> N/A                             {r}({lb}17{r}) {lb}> Profile Changer                  {r}({lb}26{r}) {lb}> Threads Spammer{r}
{r} ║   ({lb}09{r}) {lb}> N/A                       {r}║ ║   {r}({lb}18{r}) {lb}> Vanity Sniper              {r}║ ║   {r}({lb}27{r}) {lb}> Next Page  {r}                ║
{r} ╚═══                              ═══╝ ╚═══                               ═══╝ ╚═══                               ═══╝''')


banner1Theme = f'''
                                              <Xvirus Tools Self Options>
 ╔═══                              ═══╗ ╔═══                               ═══╗ ╔═══                               ═══╗
 ║   (01) > Token Login               ║ ║   (10) > Seizure                    ║ ║   (19) > Webhook Tool               ║
     (02) > Token Info                      (11) > Leave And Delete Servers         (20) > Webhook Generator
     (03) > Token Disabler                  (12) > Remove Friends                   (21) > Nitro Generator
     (04) > Token Brute-Force               (13) > Block Friends                    (22) > Server Link Generator
     (05) > Token Vc Mass Region            (14) > Dm @everyone                     (23) > Server Nuker
     (06) > Token Checker                   (15) > Delete DMs                       (24) > Group Spammer
     (07) > Token Nuker                     (16) > Clear DMs                        (25) > SelfBot Spammer
     (08) > N/A                             (17) > Profile Changer                  (26) > Threads Spammer
 ║   (09) > N/A                       ║ ║   (18) > Vanity Sniper              ║ ║   (27) > Next Page                  ║
 ╚═══                              ═══╝ ╚═══                               ═══╝ ╚═══                               ═══╝'''

def main_banner2():
    if getTheme() == "xeme":
        banner2()
    elif getTheme() == "dark":
        banner2("dark")
    elif getTheme() == "fire":
        banner2("fire")
    elif getTheme() == "aqua":
        banner2("aqua")
    elif getTheme() == "neon":
        banner2("neon")
    elif getTheme() == "rainbow":
        banner2("rainbow")

def banner2(theme=None):
    if theme == "dark":
        print(Colorate.Vertical(Colors.black_to_white, (banner2Theme)))
    elif theme == "fire":
        print(Colorate.Vertical(Colors.red_to_yellow, (banner2Theme)))
    elif theme == "aqua":
        print(Colorate.Vertical(Colors.cyan_to_blue, (banner2Theme)))
    elif theme == "neon":
        print(Colorate.Vertical(Colors.blue_to_red, (banner2Theme)))
    elif theme == "rainbow":
        print(Colorate.Horizontal(Colors.rainbow, (banner2Theme)))
    else:
        print(f'''
{r}                                            <Xvirus Tools Spammer Options>
{r} ╔═══                              ═══╗ ╔═══                               ═══╗ ╔═══                               ═══╗
{r} ║   ({lb}28{r}) {lb}> Joiner                    {r}║ ║   {r}({lb}37{r}) {lb}> Message Reactor            {r}║ ║   {r}({lb}46{r}) {lb}> N/A         {r}               ║
{r}     ({lb}29{r}) {lb}> Leaver                          {r}({lb}38{r}) {lb}> Bio Changer                      {r}({lb}47{r}) {lb}> N/A{r}
{r}     ({lb}30{r}) {lb}> Spammer                         {r}({lb}39{r}) {lb}> User Mass Friender               {r}({lb}48{r}) {lb}> N/A{r}
{r}     ({lb}31{r}) {lb}> Vc Joiner                       {r}({lb}40{r}) {lb}> Server Mass Friender             {r}({lb}49{r}) {lb}> N/A{r}
{r}     ({lb}32{r}) {lb}> Server Nickname Changer         {r}({lb}41{r}) {lb}> User Mass DM                     {r}({lb}50{r}) {lb}> N/A{r}
{r}     ({lb}33{r}) {lb}> Global Nickname Changer         {r}({lb}42{r}) {lb}> Server Mass DM                   {r}({lb}51{r}) {lb}> N/A{r}
{r}     ({lb}34{r}) {lb}> Accept Rules                    {r}({lb}43{r}) {lb}> N/A                              {r}({lb}52{r}) {lb}> N/A{r}
{r}     ({lb}35{r}) {lb}> Token Onliner                   {r}({lb}44{r}) {lb}> N/A                              {r}({lb}53{r}) {lb}> N/A{r}
{r} ║   ({lb}36{r}) {lb}> Button Presser            {r}║ ║   {r}({lb}45{r}) {lb}> N/A                         {r}║ ║  {r}({lb}54{r}) {lb}> Previous page{r}              ║
{r} ╚═══                              ═══╝ ╚═══                                ═══╝ ╚═══                              ═══╝''')


banner2Theme = f"""
                                            <Xvirus Tools Spammer Options>
 ╔═══                              ═══╗ ╔═══                               ═══╗ ╔═══                               ═══╗
 ║   (28) > Joiner                    ║ ║   (37) > Message Reactor            ║ ║   (46) > N/A                        ║
     (29) > Leaver                          (38) > Bio Changer                      (47) > N/A
     (30) > Spammer                         (39) > User Mass Friender               (48) > N/A
     (31) > Vc Joiner                       (40) > Server Mass Friender             (49) > N/A
     (32) > Server Nickname Changer         (41) > User Mass DM                     (50) > N/A
     (33) > Global Nickname Changer         (42) > Server Mass DM                   (51) > N/A
     (34) > Accept Rules                    (43) > N/A                              (52) > N/A
     (35) > Token Onliner                   (44) > N/A                              (53) > N/A
 ║   (36) > Button Presser            ║ ║   (45) > N/A                         ║ ║  (54) > Previous page              ║
 ╚═══                              ═══╝ ╚═══                                ═══╝ ╚═══                              ═══╝"""

def main_xvirus():
    if getTheme() == "xeme":
        xviruslogo()
    elif getTheme() == "dark":
        xviruslogo("dark")
    elif getTheme() == "fire":
        xviruslogo("fire")
    elif getTheme() == "aqua":
        xviruslogo("aqua")
    elif getTheme() == "neon":
        xviruslogo("neon")
    elif getTheme() == "rainbow":
        xviruslogo ("rainbow")

def xviruslogo(theme=None):
    if theme == "dark":
        print(Colorate.Vertical(Colors.black_to_white, (xviruseslogo)))
    elif theme == "fire":
        print(Colorate.Vertical(Colors.red_to_yellow, (xviruseslogo)))
    elif theme == "aqua":
        print(Colorate.Vertical(Colors.cyan_to_blue, (xviruseslogo)))
    elif theme == "neon":
        print(Colorate.Vertical(Colors.blue_to_red, (xviruseslogo)))
    elif theme == "rainbow":
        print(Colorate.Horizontal(Colors.rainbow, (xviruseslogo)))
    else:
       print(f'''{Fore.RED}
                                                                                  
                                         ,.   (   .      )        .      "        
                                       ("     )  )'     ,'        )  . (`     '`   
                                     .; )  ' (( (" )    ;(,     ((  (  ;)  "  )"  │Tokens: {token_count}
                                    _"., ,._'_.,)_(..,( . )_  _' )_') (. _..( '.. │Proxies: {proxycount}
                                    ██╗  ██╗██╗   ██╗██╗██████╗ ██╗   ██╗ ██████╗ ├─────────────
                                    ╚██╗██╔╝██║   ██║██║██╔══██╗██║   ██║██╔════╝ │Running on:
                                     ╚███╔╝ ╚██╗ ██╔╝██║██████╔╝██║   ██║╚█████╗  │{pc_username}\'s PC
                                     ██╔██╗  ╚████╔╝ ██║██╔══██╗██║   ██║ ╚═══██╗ ├─────────────
> [RPC] Toggle RPC                  ██╔╝╚██╗  ╚██╔╝  ██║██║  ██║╚██████╔╝██████╔╝ │Discord link:          
> [TM] Made by Xvirus™              ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  │.gg/xvirustool         Notes [NOTE] <
> [?] {THIS_VERSION} Changelog                                                                                    Restart [RST] <
> [!] Settings                                                                                     Manage Tokens [TKN] <''')

xviruseslogo = f'''{Fore.RED}
                                                                                  
                                         ,.   (   .      )        .      "        
                                       ("     )  )'     ,'        )  . (`     '`   
                                     .; )  ' (( (" )    ;(,     ((  (  ;)  "  )"  │Tokens: {token_count}
                                    _"., ,._'_.,)_(..,( . )_  _' )_') (. _..( '.. │Proxies: {proxycount}
                                    ██╗  ██╗██╗   ██╗██╗██████╗ ██╗   ██╗ ██████╗ ├─────────────
                                    ╚██╗██╔╝██║   ██║██║██╔══██╗██║   ██║██╔════╝ │Running on:
                                     ╚███╔╝ ╚██╗ ██╔╝██║██████╔╝██║   ██║╚█████╗  │{pc_username}\'s PC
                                     ██╔██╗  ╚████╔╝ ██║██╔══██╗██║   ██║ ╚═══██╗ ├─────────────
> [RPC] Toggle RPC                  ██╔╝╚██╗  ╚██╔╝  ██║██║  ██║╚██████╔╝██████╔╝ │Discord link:          
> [TM] Made by Xvirus™              ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  │.gg/xvirustool         Notes [NOTE] <
> [?] {THIS_VERSION} Changelog                                                                                    Restart [RST] <
> [!] Settings                                                                                     Manage Tokens [TKN] <'''

def offline():
                print(f"""{Fore.RED}







                              ██╗   ██╗ █████╗ ██╗   ██╗   █████╗ ██████╗ ███████╗
                              ╚██╗ ██╔╝██╔══██╗██║   ██║  ██╔══██╗██╔══██╗██╔════╝
                               ╚████╔╝ ██║  ██║██║   ██║  ███████║██████╔╝█████╗  
                                ╚██╔╝  ██║  ██║██║   ██║  ██╔══██║██╔══██╗██╔══╝  
                                 ██║   ╚█████╔╝╚██████╔╝  ██║  ██║██║  ██║███████╗
                                 ╚═╝    ╚════╝  ╚═════╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                               █████╗ ███████╗███████╗██╗     ██╗███╗  ██╗███████╗  ██╗
                              ██╔══██╗██╔════╝██╔════╝██║     ██║████╗ ██║██╔════╝  ██║
                              ██║  ██║█████╗  █████╗  ██║     ██║██╔██╗██║█████╗    ██║
                              ██║  ██║██╔══╝  ██╔══╝  ██║     ██║██║╚████║██╔══╝    ╚═╝
                              ╚█████╔╝██║     ██║     ███████╗██║██║ ╚███║███████╗  ██╗
                               ╚════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝╚═╝  ╚══╝╚══════╝  ╚═╝{Fore.RED}""")



logo = r"""
Please wait while Xvirus Scrapes proxies for you!










                                                        ██╗  ██╗
                                                        ╚██╗██╔╝
                                                         ╚███╔╝ 
                                                         ██╔██╗ 
                                                        ██╔╝╚██╗
                                                        ╚═╝  ╚═╝





"""[1:]


startuplogo = r"""
██╗  ██╗
╚██╗██╔╝
 ╚███╔╝ 
 ██╔██╗ 
██╔╝╚██╗
╚═╝  ╚═╝
"""[1:]




def usernamelogo():
                print(f"""







                    {Fore.RED}███████╗{Fore.BLUE}███╗  ██╗{Fore.RED}████████╗{Fore.BLUE}███████╗{Fore.RED}██████╗   {Fore.BLUE}██╗   ██╗{Fore.RED} █████╗ {Fore.BLUE}██╗   ██╗{Fore.RED}██████╗   
                    {Fore.RED}██╔════╝{Fore.BLUE}████╗ ██║{Fore.RED}╚══██╔══╝{Fore.BLUE}██╔════╝{Fore.RED}██╔══██╗  {Fore.BLUE}╚██╗ ██╔╝{Fore.RED}██╔══██╗{Fore.BLUE}██║   ██║{Fore.RED}██╔══██╗  
                    {Fore.RED}█████╗  {Fore.BLUE}██╔██╗██║{Fore.RED}   ██║   {Fore.BLUE}█████╗  {Fore.RED}██████╔╝  {Fore.BLUE} ╚████╔╝ {Fore.RED}██║  ██║{Fore.BLUE}██║   ██║{Fore.RED}██████╔╝  
                    {Fore.RED}██╔══╝  {Fore.BLUE}██║╚████║{Fore.RED}   ██║   {Fore.BLUE}██╔══╝  {Fore.RED}██╔══██╗  {Fore.BLUE}  ╚██╔╝  {Fore.RED}██║  ██║{Fore.BLUE}██║   ██║{Fore.RED}██╔══██╗  
                    {Fore.RED}███████╗{Fore.BLUE}██║ ╚███║{Fore.RED}   ██║   {Fore.BLUE}███████╗{Fore.RED}██║  ██║  {Fore.BLUE}   ██║   {Fore.RED}╚█████╔╝{Fore.BLUE}╚██████╔╝{Fore.RED}██║  ██║  
                    {Fore.RED}╚══════╝{Fore.BLUE}╚═╝  ╚══╝{Fore.RED}   ╚═╝   {Fore.BLUE}╚══════╝{Fore.RED}╚═╝  ╚═╝  {Fore.BLUE}   ╚═╝   {Fore.RED} ╚════╝ {Fore.BLUE} ╚═════╝ {Fore.RED}╚═╝  ╚═╝  

                          {Fore.BLUE}██╗   ██╗{Fore.RED} ██████╗{Fore.BLUE}███████╗{Fore.RED}██████╗ {Fore.BLUE}███╗  ██╗{Fore.RED} █████╗ {Fore.BLUE}███╗   ███╗{Fore.RED}███████╗
                          {Fore.BLUE}██║   ██║{Fore.RED}██╔════╝{Fore.BLUE}██╔════╝{Fore.RED}██╔══██╗{Fore.BLUE}████╗ ██║{Fore.RED}██╔══██╗{Fore.BLUE}████╗ ████║{Fore.RED}██╔════╝
                          {Fore.BLUE}██║   ██║{Fore.RED}╚█████╗ {Fore.BLUE}█████╗  {Fore.RED}██████╔╝{Fore.BLUE}██╔██╗██║{Fore.RED}███████║{Fore.BLUE}██╔████╔██║{Fore.RED}█████╗  
                          {Fore.BLUE}██║   ██║{Fore.RED} ╚═══██╗{Fore.BLUE}██╔══╝  {Fore.RED}██╔══██╗{Fore.BLUE}██║╚████║{Fore.RED}██╔══██║{Fore.BLUE}██║╚██╔╝██║{Fore.RED}██╔══╝  
                          {Fore.BLUE}╚██████╔╝{Fore.RED}██████╔╝{Fore.BLUE}███████╗{Fore.RED}██║  ██║{Fore.BLUE}██║ ╚███║{Fore.RED}██║  ██║{Fore.BLUE}██║ ╚═╝ ██║{Fore.RED}███████╗
                          {Fore.BLUE} ╚═════╝ {Fore.RED}╚═════╝ {Fore.BLUE}╚══════╝{Fore.RED}╚═╝  ╚═╝{Fore.BLUE}╚═╝  ╚══╝{Fore.RED}╚═╝  ╚═╝{Fore.BLUE}╚═╝     ╚═╝{Fore.RED}╚══════╝
                                                                                                 """)

username = get_username()
#######################################################################################################################

def toggle_proxy_scraper():
    file_path = os.path.join(os.getenv("TEMP"), 'xvirus_proxy_settings')
    
    with open(file_path, 'r') as f:
        current_setting = f.read().strip()
    
    if current_setting == 'y':
        new_setting = 'n'
        print(f"{Fore.RED} <*> Proxy Scraping Toggled {Fore.BLUE}OFF")
        sleep(1)
    else:
        new_setting = 'y'
        print(f"{Fore.RED} <*> Proxy Scraping Toggled {Fore.BLUE}ON")
        sleep(1)
    
    with open(file_path, 'w') as f:
        f.write(new_setting)

def clear_proxy_cache():
    file_path = os.path.join(os.getenv("TEMP"), 'xvirus_proxies')
    
    with open(file_path, 'w') as f:
        f.write('')

    print(f"{Fore.RED} <*> Proxy Cache Cleared")
    sleep(1)   

def add_own_proxies():
    txt_path = input(f'{Fore.RED} <~> Enter the path to the txt file containing proxies: {Fore.BLUE}')
    file_path = os.path.join(os.getenv("TEMP"), 'xvirus_proxies')
    clear_proxy_cache()
    
    with open(txt_path, 'r') as txt_file:
        proxies = txt_file.read()
    
    with open(file_path, 'w') as f:
        f.write(proxies)
    
    print(f"{Fore.RED} <*> Successfully Wrote New Proxies")
    sleep(1)   

def settings():
    print(f'''
        {Fore.BLUE}[{Fore.RED}1{Fore.BLUE}] Theme changer
        {Fore.BLUE}[{Fore.RED}2{Fore.BLUE}] Change Username
        {Fore.BLUE}[{Fore.RED}3{Fore.BLUE}] Go Into GUI Mode
        {Fore.BLUE}[{Fore.RED}4{Fore.BLUE}] Proxy Settings
        {Fore.BLUE}[{Fore.RED}5{Fore.BLUE}] {Fore.RED}Exit...    
                        ''')
    secondchoice = input(f'{Fore.RED} <~> Setting: {Fore.BLUE}')
    if secondchoice not in ["1", "2", "3", "4", "5"]:
        print(f'{Fore.RED} <!> Invalid Setting')
        sleep(1)
    if secondchoice == "1":
        print(f"\n{Fore.RED}    Xeme: 1")
        print(Colorate.Horizontal(Colors.white_to_black, "    Dark: 2", 1))
        print(Colorate.Horizontal(Colors.yellow_to_red, "    Fire: 3", 3))
        print(Colorate.Horizontal(Colors.cyan_to_blue, "    Aqua: 4", 3))
        print(Colorate.Horizontal(Colors.blue_to_red, "    Neon: 5", 3))
        print(Colorate.Horizontal(Colors.rainbow, "    Rainbow: 6", 5))
        themechoice = input(f'\n{Fore.RED} <~> Theme: {Fore.BLUE}')
        if themechoice == "1":
            setTheme('xeme')
        elif themechoice == "2":
            setTheme('dark')
        elif themechoice == "3":
            setTheme('fire')
        elif themechoice == "4":
            setTheme('aqua')
        elif themechoice == "5":
            setTheme('neon')
        elif themechoice == "6":
            setTheme('rainbow')
        else:
            print(f'{Fore.RED} <!> Invalid Theme')
            sleep(1.5)
        print_slow(f"{Fore.RED} <*> Theme set to {Fore.BLUE}{getTheme()}")
        sleep(0.5)

    elif secondchoice == "2":
        new_username = input(f'{Fore.BLUE} <~> Enter your new username: ')
        setUsername(new_username)
        print_slow(f"{Fore.RED} <*> Username set to {Fore.BLUE}{new_username}\n{Fore.RED} <!> Restarting tool")
        sleep(2)
        subprocess.run("Xvirus-Tools.exe", shell=True)
        exit()

    elif secondchoice == "3":
        print_slow(f"{Fore.RED} <!> This Option was removed due to a bug it will be implemented later!")
        PETC()

    elif secondchoice == "4":
        print(f"""
    {Fore.BLUE}[{Fore.RED}1{Fore.BLUE}] Toggle Proxy Scraper
    {Fore.BLUE}[{Fore.RED}3{Fore.BLUE}] Clear Proxy Cache
    {Fore.BLUE}[{Fore.RED}4{Fore.BLUE}] Add own Proxies to Cache
    """)
        proxychoice = input(f'{Fore.RED} <~> Choice: {Fore.BLUE}')
        if proxychoice == '1':
            toggle_proxy_scraper()
        elif proxychoice == '2':
            clear_proxy_cache()
        elif proxychoice == '3':
            add_own_proxies()
        else:
            print(f"{Fore.RED} <!> Invalid Choice")

    elif secondchoice == "5":
        SetTitle("Exiting")
        choice = input(f'{Fore.RED} <~> Are you sure you want to exit? (Y to confirm): {Fore.BLUE}')
        if choice.upper() == 'Y':
            clear()
            os._exit(0)
        else:
            sleep(0.5)
    else:
        clear()

class DiscordProps:
    @staticmethod
    def get_build_number():
        scripts = re.compile(r'/assets/.{20}.js', re.I).findall(requests.get("https://discord.com/app", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}).text)
        scripts.reverse()
        for v in scripts:
            content = requests.get(f"https://discord.com{v}", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}).content.decode()
            if content.find("build_number:\"") != -1:
                return re.compile(r"build_number:\"(.*?)\"", re.I).findall(content)[0]
    user_agents = [
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
    ]
    lang = [
        "de,de-DE;q=0.9",
        "en,en-US;q=0.9",
        "es,es-ES;q=0.9",
        "fr,fr-FR;q=0.9",
        "ja;q=0.9",
        "ru,ru-RU;q=0.9",
        "pt-BR;q=0.9",
        "tr;q=0.9",
        "ar,ar-SA;q=0.9",
        "zh,zh-CN;q=0.9"
    ]
    brands = [
        """Not?A_Brand";v="8", "Chromium";v="108""",
        """Not?A_Brand";v="8", "Firefox";v="92""",
        """Not?A_Brand";v="8", "Safari";v="15""",
        """Edge";v="96", "Chromium";v="108""",
        """Brave";v="1.31", "Chromium";v="108""",
        """Opera";v="88", "Chromium";v="108""",
        """Internet Explorer";v="11", "Chromium";v="108"""
    ]
    channels = [
        "ptb", 
        "canary", 
        "stable"
    ] 
    times = [
        "Europe/Berlin",
        "America/New_York",
        "Asia/Tokyo",
        "Australia/Sydney",
        "America/Los_Angeles",
        "Africa/Cairo",
        "Asia/Dubai",
        "America/Mexico_City",
        "Pacific/Auckland",
        "America/Chicago"
    ]
    zone = random.choice(times)
    channels = ["ptb", "canary", "stable"] 
    user_agent = random.choice(user_agents)
    language = random.choice(lang)
    channel = random.choice(channels)  
    buildNumber = get_build_number()
    x_super_properties = base64.b64encode(json.dumps({
        "os": "Windows",
        "browser": "Discord Client",
        "release_channel": channel,
        "client_version": "1.0.9011",
        "os_version": "10.0.22638",
        "os_arch": "x64",
        "system_locale": "en",
        "client_build_number": buildNumber,
        "native_build_number": 30306,
        "client_version_string": "1.0.9011",
        "os_version_string": "10.0.22638",
        "os_arch_string": "x64"}).encode()).decode()
    
    bypassheaders = {
        'authority': 'discord.com',
        'x-super-properties': x_super_properties,
        'x-discord-locale': 'en',
        'x-debug-options': 'bugReporterEnabled',
        'accept-language': 'en',
        'user-agent': user_agent,
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://discord.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        }
    
    default_headers = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': language,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': zone,
        'x-super-properties': x_super_properties,
    }

class Header:
    @staticmethod
    def tls_session() -> tls_client.Session:
        client = tls_client.Session(
            client_identifier=f"chrome_{random.randint(110, 116)}",
            random_tls_extension_order=True,
            ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,10-23-27-43-13-65281-16-5-45-18-0-11-35-17513-51-21-41,29-23-24,0",
            h2_settings={
                "HEADER_TABLE_SIZE": 65536,
                "MAX_CONCURRENT_STREAMS": 1000,
                "MAX_HEADER_LIST_SIZE": 262144,
                "INITIAL_WINDOW_SIZE": 6291456     
            },
            h2_settings_order=[
                "HEADER_TABLE_SIZE",
                "MAX_CONCURRENT_STREAMS",
                "INITIAL_WINDOW_SIZE",
                "MAX_HEADER_LIST_SIZE"
            ],
            supported_signature_algorithms=[
                "PKCS1WithSHA384",
                "PSSWithSHA512",
                "PKCS1WithSHA512",
                "ECDSAWithP256AndSHA256",
                "PSSWithSHA256",
                "PKCS1WithSHA256",
                "ECDSAWithP384AndSHA384",
                "PSSWithSHA384",
            ],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
            connection_flow=15663105,
            header_order=["accept", "user-agent", "accept-encoding", "accept-language"]
        )
        
        return client

    @staticmethod
    def get_cookies(session, headers):
        cookies = dict(
            session.get("https://discord.com", headers=headers).cookies
        )

        cookies["__cf_bm"] = (
            "0duPxpWahXQbsel5Mm.XDFj_eHeCKkMo.T6tkBzbIFU-1679837601-0-"
            "AbkAwOxGrGl9ZGuOeBGIq4Z+ss0Ob5thYOQuCcKzKPD2xvy4lrAxEuRAF1Kopx5muqAEh2kLBLuED6s8P0iUxfPo+IeQId4AS3ZX76SNC5F59QowBDtRNPCHYLR6+2bBFA=="
        )
        cookies["locale"] = "en-US"

        return cookies

    @staticmethod
    def get_client(token):
        default_headers = DiscordProps.default_headers.copy()
        default_headers["authorization"] = token

        session = Header.tls_session()
        cookie = Header.get_cookies(session, headers=default_headers)
    
        default_headers["cookie"] = (
            f'__dcfduid={cookie["__dcfduid"]}; '
            f'__sdcfduid={cookie["__sdcfduid"]}; '
            f'__cfruid={cookie["__cfruid"]}; '
            f'__cf_bm={cookie["__cf_bm"]}; '
            f'locale={cookie["locale"]}'
        )
    
        return session, default_headers, cookie

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
    
def get_random_id(id):
    file = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_ids")
    with open(file, "r", encoding="utf8") as f:
        users = [line.strip() for line in f.readlines()]
    randomid = random.sample(users, id)
    return "<@!" + "> <@!".join(randomid) + ">"

def get_ids():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_ids")

    if not os.path.exists(temp_folder):
        return []

    with open(temp_folder, "r") as f:
        ids = f.read().strip().splitlines()

    ids = [idd for idd in ids if idd.strip()]

    if not ids:
        print(f"{Fore.RED} <!> No ids Were Found In The Cache")

    return ids

def rand_str(length:int) -> str:
    return ''.join(random.sample(string.ascii_lowercase+string.digits, length))

file = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_ids")
class WebSocket(websocket.WebSocket):
    
    def __init__(self, token, guild_id, channel_id):
        self.MAX_ITER = 10
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.socket_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": DiscordProps.user_agent,
        }
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            #header=self.socket_headers,
            on_open=lambda ws: self.sock_open(ws),
            on_message=lambda ws, msg: self.sock_message(ws, msg),
            on_close=lambda ws, close_code, close_msg: self.sock_close(
                ws, close_code, close_msg
            ),
        )
        self.endScraping = False
        self.guilds = {}
        self.members: list[str] = []
        self.ranges = [[0]]
        self.lastRange = 0
        self.packets_recv = 0
        self.msgs = []
        self.d = 1
        self.iter = 0
        self.big_iter = 0
        self.finished = False

    def getRanges(self, index, multiplier, memberCount):
        initialNum = int(index * multiplier)
        rangesList = [[initialNum, initialNum + 99]]
        if memberCount > initialNum + 99:
            rangesList.append([initialNum + 100, initialNum + 199])
        if [0, 99] not in rangesList:
            rangesList.insert(0, [0, 99])
        return rangesList

    def parseGuildMemberListUpdate(self, response):
        memberdata = {
            "online_count": response["d"]["online_count"],
            "member_count": response["d"]["member_count"],
            "id": response["d"]["id"],
            "guild_id": response["d"]["guild_id"],
            "hoisted_roles": response["d"]["groups"],
            "types": [],
            "locations": [],
            "updates": [],
        }
        
        for chunk in response["d"]["ops"]:
            memberdata["types"].append(chunk["op"])
            if chunk["op"] in ("SYNC", "INVALIDATE"):
                memberdata["locations"].append(chunk["range"])
                if chunk["op"] == "SYNC":
                    memberdata["updates"].append(chunk["items"])
                else:
                    memberdata["updates"].append([])
            elif chunk["op"] in ("INSERT", "UPDATE", "DELETE"):
                memberdata["locations"].append(chunk["index"])
                if chunk["op"] == "DELETE":
                    memberdata["updates"].append([])
                else:
                    memberdata["updates"].append(chunk["item"])
        return memberdata

    def find_most_reoccuring(self, list):
        return max(set(list), key=list.count)

    def run(self) -> list[str]:
        try:
            self.run_forever()
            self.finished = True
            return self.members
        except Exception as e:
            print(e)
            pass

    def scrapeUsers(self):
        if self.endScraping == False:
            self.send(
                '{"op":14,"d":{"guild_id":"'
                + self.guild_id
                + '","typing":true,"activities":true,"threads":true,"channels":{"'
                + self.channel_id
                + '":'
                + json.dumps(self.ranges)
                + "}}}"
            )

    def sock_open(self, ws):
        self.send(
            '{"op":2,"d":{"token":"'
            + self.token
            + '","capabilities":125,"properties":{"os":"Windows","browser":"Firefox","device":"","system_locale":"it-IT","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}'
        )

    def heartbeatThread(self, interval):
        try:
            while True:
                self.send('{"op":1,"d":' + str(self.packets_recv) + "}")
                time.sleep(interval)
        except Exception as e:
            return

    def sock_message(self, ws, message):
        try:
            decoded = json.loads(message)
            if decoded is None:
                return
            if decoded["op"] != 11:
                self.packets_recv += 1
            if decoded["op"] == 10:
                threading.Thread(
                    target=self.heartbeatThread,
                    args=(decoded["d"]["heartbeat_interval"] / 1000,),
                    daemon=True,
                ).start()
            if decoded["t"] == "READY":
                for guild in decoded["d"]["guilds"]:
                    self.guilds[guild["id"]] = {"member_count": guild["member_count"]}
            if decoded["t"] == "READY_SUPPLEMENTAL":
                self.ranges = self.getRanges(
                    0, 100, self.guilds[self.guild_id]["member_count"]
                )
                self.scrapeUsers()
            elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
                parsed = self.parseGuildMemberListUpdate(decoded)
                self.msgs.append(len(self.members))
                print(f"{Fore.BLUE} <*> Scraped {Fore.RED}{len(self.members)}{Fore.BLUE} members", end="\r")
                if self.d == len(self.members):
                    self.iter += 1
                    if self.iter == self.MAX_ITER:
                        print(f"{Fore.BLUE} <*> Scraped {Fore.RED}{len(self.members)}{Fore.BLUE} members")
                        self.endScraping = True
                        self.close()
                        return
                self.d = self.find_most_reoccuring(self.msgs)
                if parsed["guild_id"] == self.guild_id and (
                    "SYNC" in parsed["types"] or "UPDATE" in parsed["types"]
                ):
                    for (elem, index) in enumerate(parsed["types"]):
                        if index == "SYNC":
                            for item in parsed["updates"]:
                                if len(item) > 0:
                                    for member in item:
                                        if "member" in member:
                                            mem = member["member"]
                                            obj = {
                                                "tag": mem["user"]["username"]
                                                + "#"
                                                + mem["user"]["discriminator"],
                                                "id": mem["user"]["id"],
                                            }
                                            if not mem["user"].get("bot"):
                                                self.members.append(str(mem["user"]["id"]))
                        elif index == "UPDATE":
                            for item in parsed["updates"][elem]:
                                if "member" in item:
                                    mem = item["member"]
                                    obj = {
                                        "tag": mem["user"]["username"]
                                        + "#"
                                        + mem["user"]["discriminator"],
                                        "id": mem["user"]["id"],
                                    }
                                    if not mem["user"].get("bot"):
                                        self.members.append(str(mem["user"]["id"]))
                        self.lastRange += 1
                        self.ranges = self.getRanges(
                            self.lastRange, 100, self.guilds[self.guild_id]["member_count"]
                        )
                        time.sleep(0.45)
                        self.scrapeUsers()
                if self.endScraping:
                    print(f"{Fore.BLUE} <*> Scraped {Fore.RED}{len(self.members)}{Fore.BLUE} members")
                    self.close()
        except Exception as e:
            print(e)

def reset_ids():
    if os.path.exists(file):
        os.remove(file)

def scrape_id(token, guild_id, channel_id):
        return WebSocket(token, guild_id, channel_id).run()

def get_random_token():
    tokens = get_tokens()
    if tokens:
        return random.choice(tokens)
    else:
        return None

def id_scraper():
    reset_ids()
    guild_id = input(f"{Fore.RED} <~> guild id: {Fore.BLUE}")
    channel_id = input(f"{Fore.RED} <~> channel id: {Fore.BLUE}")
    
    token = get_random_token()
    
    users = scrape_id(token, guild_id, channel_id)
    with open(file, "w") as f:
        for user in users:
            f.write(f"{user}\n")
        
    print(f"{Fore.BLUE} <*> Scraped {len(users)} ids")

def create_settings_file(file_path):
    with open(file_path, 'w') as file:
        file.write('n')