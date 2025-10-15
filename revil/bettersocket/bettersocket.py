import sys
import socket
import tty
import termios
import select
import os


def interactive(sock):
    """Attach the given connected socket to the local terminal interactively."""

    # --- Save and set terminal to raw mode ---
    old_tty = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    tty.setcbreak(sys.stdin.fileno())

    try:
        while True:
            # Monitor both stdin (fd 0) and the socket
            rlist, _, _ = select.select([sys.stdin, sock], [], [])

            # If there's data from stdin, send it to the socket
            if sys.stdin in rlist:
                data = os.read(sys.stdin.fileno(), 1024)
                if not data:
                    break  # EOF
                sock.sendall(data)

            # If there's data from the socket, write it to stdout
            if sock in rlist:
                try: # There is a bug which just breaks here. Maybe this try/except fixes this
                    data = sock.recv(1024)
                except Exception:
                    pass
                if not data:
                    break  # Connection closed
                os.write(sys.stdout.fileno(), data)
    finally:
        # --- Restore terminal settings ---
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
