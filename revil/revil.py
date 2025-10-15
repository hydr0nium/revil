import argparse
import socket
import random
import os
from revil.bettersocket import bettersocket

def get_socket(args):
    for _ in range(100):
        sport = random.randint(1,1023)
        if args.noroot:
            sport = random.randint(1030,10000)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The default is on purpose quite high as the old implementations
        # cat take quite a long time to answer for the first time. Default: 100
        s.settimeout(args.timeout)
        try:
            s.bind(('', sport))
            return s
        except OSError:
            s.close()
    print("[-] Could not get a free privileged source port!")
    exit()


def rlogin(args):
  
    username = args.user
    connection = (args.host, args.port)
    s = get_socket(args)
    s.connect(connection)

    # Send login packet
    s.send(b"\00" + username.encode() + b"\00" + username.encode() + b"\x00xterm/38400\x00")
    try:
        s.recv(1)
    except socket.timeout as _:
        print(f"[-] Could not connect to: {ip}")
        s.close()
        exit()
    s.settimeout(300)
    bettersocket.interactive(s)
    s.close()


def rsh(args): 
    username = args.user
    connection = (args.host, args.port)
    s = get_socket(args)
    s.connect(connection)
    # this is another test
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
        s.close()
        exit()
    s.close()

def main():
    parser = setup_parser()
    args = parser.parse_args()
    if "noroot" not in args or not args.noroot:
        check_root()
    match args.subcommand:
        case "rlogin":
            rlogin(args)
        case "rsh":
            rsh(args)
        case "rexec":
            raise NotImplemented
        case _:
            parser.print_help()


def check_root():
    if os.getuid() != 0:
        print("[-] Some old r-command server require that the client connects with a privileged port.")
        print("[-] For this root access is needed.")
        print("[-] I try my best to be careful on what I do to not abuse the root rights.")
        print("[-] Still be careful what you run as root. In any case. Always check the source.")
        print("[-] You can suppress this warning and run without root anyway with: --noroot")
        print("[-] Note though that this could make the server reject your connection.")
        exit(1)

def setup_parser():
    parser = argparse.ArgumentParser(prog="Revil")
    subparser = parser.add_subparsers(dest='subcommand')

    parser_rlogin = subparser.add_parser("rlogin", help="Use rlogin")
    parser_rlogin.add_argument('-u', '--user', required=True, dest='user', help="The user to login to. This will automatically spoof the source user as well")
    parser_rlogin.add_argument("-p", '--port', type=int, default=513, dest="port", help="The port to connect to (Default: 513)")
    parser_rlogin.add_argument('-t', '--timeout', type=int, default=100, dest="timeout", help="Timeout (in seconds) of the initial connection (Default: 100)")
    parser_rlogin.add_argument("-nr", "--noroot", action="store_true", dest="noroot", help="Run revil as non root user")
    parser_rlogin.add_argument('host', help="The host / ip to connect to")

    parser_rsh = subparser.add_parser("rsh", help="Use rsh")
    parser_rsh.add_argument('-u', '--user', required=True, dest='user', help="The user to login to. This will automatically spoof the source user as well")
    parser_rsh.add_argument("-p", '--port', type=int, default=514, dest="port", help="The port to connect to (Default: 514)")
    parser_rsh.add_argument('-t', '--timeout', type=int, default=100, dest="timeout", help="Timeout (in seconds) of the initial connection (Default: 100)")
    parser_rsh.add_argument("-nr", "--noroot", action="store_true", dest="noroot", help="Run revil as non root user")
    parser_rsh.add_argument('host', help="The host / ip to connect to")
    parser_rsh.add_argument('command', help="the command that is executed on the target")

    parser_rexec = subparser.add_parser("rexec", help="Use rexec")
    parser_rexec.add_argument('-u', '--user', required=True, dest='user', help="The user to login to. This will automatically spoof the source user as well")
    parser_rexec.add_argument("-p", '--port', type=int, default=514, dest="port", help="The port to connect to (Default: 514)")
    parser_rexec.add_argument('-t', '--timeout', type=int, default=100, dest="timeout", help="Timeout (in seconds) of the initial connection (Default: 100)")
    parser_rexec.add_argument("-nr", "--noroot", action="store_true", dest="noroot", help="Run revil as non root user")
    parser_rexec.add_argument('host', help="The host / ip to connect to")

    parser_rwho = subparser.add_parser("rwho", help="Use rwho")
    parser_rwho.add_argument('-u', '--user', required=True, dest='user', help="The user to login to. This will automatically spoof the source user as well")
    parser_rwho.add_argument("-p", '--port', type=int, default=514, dest="port", help="The port to connect to (Default: 514)")
    parser_rwho.add_argument('-t', '--timeout', type=int, default=100, dest="timeout", help="Timeout (in seconds) of the initial connection (Default: 100)")
    parser_rwho.add_argument("-nr", "--noroot", action="store_true", dest="noroot", help="Run revil as non root user")
    parser_rwho.add_argument('host', help="The host / ip to connect to")
    return parser


if __name__ == "__main__":
    main()
