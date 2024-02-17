import ctypes
import hashlib
import os
import sys
from ctypes import wintypes
from datetime import datetime
from time import sleep
import psutil

from colorama import Fore
from util import *

#note: was too lazy to make the patch for a whitelister on a dll base 

def list_loaded_dlls():
    pid = os.getpid()
    process = psutil.Process(pid)

    dll_list = []
    for lib in process.memory_maps():
        if lib.path and lib.path.endswith(".dll"):
            dll_list.append(lib.path)
    return dll_list

def get_checksum():
    md5_hash = hashlib.md5()
    with open("".join(sys.argv), "rb") as file:
        md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

def save_key_to_file(key):
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_key")
    with open(temp_folder, "w") as key_file:
        key_file.write(key)

def read_key_from_file():
    temp_folder = os.path.join(os.environ.get("TEMP", "C:\\temp"), "xvirus_key")
    if os.path.exists(temp_folder):
        with open(temp_folder, "r") as key_file:
            return key_file.read().strip()
    return None

auth = api(
    name="xvirus",
    ownerid="H1Blx2txmS",
    secret="f8a86b6a889a4c6da214ceabc99fedffbbe464adb64d7df87934afb70625ad92",
    version="1.0",
    hash_to_check=get_checksum())

def license_check():
    saved_key = read_key_from_file()
    if saved_key:
            auth.license(saved_key)
            print(f"{Fore.BLUE}Welcome Back {pc_username}!")
            sleep(2)
    else:
        ask_for_key()

def ask_for_key():
        key = input(f"{Fore.RED}Enter your Xvirus License Key: {Fore.BLUE}")
        auth.license(key)
        save_key_to_file(key)
        print(f"{Fore.BLUE} <*> Welcome Back {pc_username}!")
        sleep(2)

threads = 5
current_dir = os.path.dirname(os.path.abspath(__file__))
               
def main1():
    SetTitle(f"Xvirus {THIS_VERSION}")
    global threads
    clear()
    main_xvirus()
    main_banner1()
    choice = input(f'''{Fore.RED} ┌──<{username}@Xvirus>─[~]
 └──╼ $ {Fore.BLUE}''').lstrip("0")
    choice = choice.upper()

    if choice == "1":
        WIP()#tokenLogin()
        PETC()
        main1()

    elif choice == '2':
        getinfo()
        PETC()
        main1()

    elif choice == '3':
        TokenDisabler()
        PETC()
        main1()        

    elif choice == '4':
        tokenbrute()
        PETC()
        main1()

    elif choice == '5':
        regionChanger()
        PETC()
        main1()

    elif choice == '6':
        checktokens()
        PETC()
        main1()

    elif choice == '7':
        Xvirus_Nuke()
        PETC()
        main1()

    elif choice == '8':
        WIP()
        PETC()
        main1()

    elif choice == '9':
        PETC()
        main1()

    elif choice == '10':
        Seizure()
        PETC()
        main1()

    elif choice == '11':
        Leaver()
        PETC()
        main1()

    elif choice == '12':
        UnFriender()
        PETC()
        main1()

    elif choice == '13':
        BlockAll()
        PETC()
        main1()

    elif choice == '14':
        massdm()
        PETC()
        main1()

    elif choice == '15':
        deletedms()
        PETC()
        main1()

    elif choice == "16":
        dmclearer()
        PETC()
        main1()

    elif choice == '17':
        ProfileChanger()
        PETC()
        main1()

    elif choice == '18':
        snipe()
        PETC()
        main1()

    elif choice == '19':
        webhooktool()
        PETC()
        main1()

    elif choice == '20':
        webhookegen()
        PETC()
        main1()

    elif choice == '21':
        nitrogenerator()
        PETC()
        main1()
        
    elif choice == '22':
        serverlinkgen()
        PETC()
        main1()

    elif choice == '23':
        servernuker()
        PETC()
        main1()

    elif choice == '24':
        groupspammer()
        PETC()
        main1()

    elif choice == '25':
       selfbotspammer()
       PETC()
       main1()

    elif choice == '26':
        threadSpammer()
        PETC()
        main1()

    elif choice == '27':
        main2()

    elif choice == '?':
        CHANGE_LOG()
        PETC()
        main1()

    elif choice == 'TM':
            print(f'''
        {Fore.BLUE}[{Fore.RED}Github{Fore.BLUE}] @DXVVAY(DEXV), @Xvirus0, @2l2cgit(AdminX)
        {Fore.BLUE}[{Fore.RED}Twitter{Fore.BLUE}] @dexvisnotgay
        {Fore.BLUE}[{Fore.RED}Discord{Fore.BLUE}] .gg/xvirustool, @dexvmaster, @adminxfr
                    ''')
            PETC()
            main1()
    
    elif choice == 'RST':
        restart()

    elif choice == 'TKN':
        savetokens()
        PETC()
        main1()

    elif choice == 'NOTE':
        VERSION_NOTES()
        PETC()
        main1()

    elif choice == '!':
        settings()
        main1()

    elif choice == 'RPC':
        toggle_rpc()
        main1()

    elif choice == 'DLLC':
        loaded_dlls = list_loaded_dlls()

        dll_count = len(loaded_dlls)

        if dll_count > 88:
            print("BUY XVIRUS NOT CRACK IT L")
            sys.exit(1)
        elif dll_count > 0:
            pass
        else:
            print("No DLLs found in the current process.")

    else:
        print_slow(" <!> Invalid option. Please choose a valid option.")
        sleep(1.5)
        main1()

def main2():
    SetTitle(f"Xvirus {THIS_VERSION}")
    global threads
    clear()
    main_xvirus()
    main_banner2()
    choice = input(f'''{Fore.RED} ┌──<{username}@Xvirus>─[~]
 └──╼ $ {Fore.BLUE}''').lstrip("0")
    choice = choice.upper()

    if choice == '28':
        joiner()
        PETC()
        main2()

    elif choice == '29':
        serverLeaver()
        PETC()
        main2()

    elif choice == '30':
        raider()
        PETC()
        main2()

    elif choice == '31':
        vcjoiner()
        PETC()
        main2()
    
    elif choice == '32':
        ServerNicker()
        PETC()
        main2()
    
    elif choice == '33':
        tokenNicker()
        PETC()
        main2()
    
    elif choice == '34':
        AcceptRules()
        PETC()
        main2()
    
    elif choice == '35':
        onliner()
        PETC()
        main2()
    
    elif choice == '36':
        buttonPresser()
        PETC()
        main2()

    elif choice == '37':
        reactor()
        PETC()
        main2()
    
    elif choice == '38':
        TokenBioSet()
        PETC()
        main2()
    
    elif choice == '39':
        userFriender()
        PETC()
        main2()
    
    elif choice == '40':
        ServerFriendReq()
        PETC()
        main2()

    elif choice == '41':
        massdm()
        PETC()
        main2()
    
    elif choice == '42':
        WIP()
        PETC()
        main2()

    elif choice == '54':
        main1()

    elif choice == '?':
        CHANGE_LOG()
        PETC()
        main2()

    elif choice == 'TM':
            print(f'''
        {Fore.BLUE}[{Fore.RED}Github{Fore.BLUE}] @DXVVAY(DEXV), @Xvirus0, @2l2cgit(AdminX)
        {Fore.BLUE}[{Fore.RED}Twitter{Fore.BLUE}] @dexvisnotgay
        {Fore.BLUE}[{Fore.RED}Discord{Fore.BLUE}] .gg/xvirustool, @dexvmaster, @adminxfr
                    ''')
            PETC()
            main2()
    
    elif choice == 'RST':
        restart()
    
    elif choice == 'TKN':
        savetokens()
        PETC()
        main2()

    elif choice == 'NOTE':
        VERSION_NOTES()
        PETC()
        main2()

    elif choice == '!':
        settings()
        main2()

    elif choice == 'RPC':
        toggle_rpc()
        main2()

    else:
        print_slow(" <!> Invalid option. Please choose a valid option.")
        sleep(1.5)
        main2()


if __name__ == "__main__":
    file_path = os.path.join(os.getenv("temp"), 'xvirus_proxy_settings')
    SetTitle("Xvirus Loading")
    set_terminal_width(xvirus_width)
    check_wifi_connection()
    WebText()
    search_for_updates()
    license_check()
    loaded_dlls = list_loaded_dlls()
    dll_count = len(loaded_dlls)
    if dll_count > 94:
        print("BUY XVIRUS NOT CRACK IT L")
        sleep(2)
        sys.exit(1)
    elif dll_count > 0:
        pass
    else:
        print("No DLLs found in the current process.")
    get_username()
    check_version()
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if content == 'y':
                proxy_scrape()
            elif content == 'n':
                pass
            else:
                print(" <!> Invalid content in xvirus proxy settings")
    else:
        create_settings_file(file_path)
        print(" <*> setting file created")
    if not os.path.exists(os.getenv("temp") + "\\xvirus_theme"):
        setTheme('xeme')
    sleep(1.5)
    main1()