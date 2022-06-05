import argparse
import sys
import textwrap
from Netcat import Netcat


if __name__ == '__main__':
    buffer: str = ''
    parser = argparse.ArgumentParser(
    description="NetCat written in python, jow!!!",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent("""
        Use the examples:
        python Main.py -t 192.168.2.10 -p 5555 -l -c [interative shell :) good luck! ]
        python Main.py -t 192.168.2.10 -p 5555 -l -u=test.txt [upload file]
        python Main.py -t 192.168.2.10 -p 5555 -l -e=[comand]
        python Main.py -t 192.168.2.10 -p 5555 [connect to server at 5555 port, for example]
    """)
    )
    parser.add_argument('-t', "--target", type=str, help='specific a ip address', required=True)
    parser.add_argument('-p', "--port", type=int, help='specific a port', required=True)
    parser.add_argument('-c', "--command", action='store_true', help='command shell')
    parser.add_argument('-l', "--listen", action='store_true',help='listen for connections')
    parser.add_argument('-e', "--execute", help='command shell')
    parser.add_argument('-u', "--upload", action='store_true', help='upload file')
    args = parser.parse_args()
    if not args.listen:  # se não for listen, abre entradas para o console
        buffer = sys.stdin.read()
    net_cat = Netcat(args, buffer.encode())
    net_cat.start()
