import argparse
import socket
from revil.bettersocket import bettersocket

def rlogin(args):

    SOURCE_PORT = 1023  
    username = args.user
    port = 513
    if args.port:
        port = args.port
    connection = (args.host, port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(100)
    s.bind(('', SOURCE_PORT)) # Set up the source port to be < 1024 because rlogin wants that
    s.connect(connection)

    # Send login packet
    s.send(b"\00" + username.encode() + b"\00" + username.encode() + b"\x00xterm/38400\x00")
    try:
        s.recv(1)
    except socket.timeout as _:
        print(f"[-] Could not connect to: {ip}")
        exit()
    s.settimeout(300)
    bettersocket.interactive(s)


def rsh(args): 
    SOURCE_PORT = 1023  
    username = args.user
    port = 514
    if args.port:
        port = args.port
    connection = (args.host, port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(100)
    s.bind(('', SOURCE_PORT)) # Set up the source port to be < 1024 because rlogin wants that
    s.connect(connection)

    # Send login packet
    s.send(b"\00" + username.encode() + b"\00" + username.encode() + b"\x00"+ args.command.encode() + b"\x00")
    try:
        status = s.recv(1)
        output = s.recv(4096)
        if status != b"\x00":
            print("[-] There was an error while connecting")
        print(output.decode())
    except socket.timeout as _:
        print(f"[-] Could not connect to: {ip}")
        exit()

def main():
    parser = argparse.ArgumentParser(prog="Revil")
    subparser = parser.add_subparsers(dest='subcommand')

    parser_rlogin = subparser.add_parser("rlogin", help="Use rlogin")
    parser_rlogin.add_argument('-u', '--user', required=True, dest='user')
    parser_rlogin.add_argument("-P", '--port', dest="port")
    parser_rlogin.add_argument('host')

    parser_rsh = subparser.add_parser("rsh", help="Use rsh")
    parser_rsh.add_argument('-u', '--user', required=True, dest='user')
    parser_rsh.add_argument("-P", '--port', dest="port")
    parser_rsh.add_argument('host')
    parser_rsh.add_argument('command')

    args = parser.parse_args()
    match args.subcommand:
        case "rlogin":
            rlogin(args)
        case "rsh":
            rsh(args)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
