import sys
import threading
from argparse import Namespace
import socket

from ExecuteRemoteCommands import execute


class Netcat:
    """
    A utility capable of establishing a TCP or UDP connection between
    two computers, meaning it can write and read through an open port.
    With the help of the program, files can be transferred and commands
    can be executed in some instances.
    """
    def __init__(self, args: Namespace, buffer: bytes) -> None:
        """
        :param args:
        :param buffer:
        """
        self.__args = args
        self.__buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @property
    def args(self) -> Namespace:
        return self.__args

    @property
    def buffer(self) -> bytes:
        return self.__buffer

    def start(self) -> None:
        print(self.args)
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self) -> None:
        # send data
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        recv_len: int = 1
        response: int = ''
        print("DSA")
        try:
            while True:
                while recv_len:
                    data: bytes = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(f"Target device says: {response}")
                    buffer = input("> ")  # apos receber a resposta, permite enviar um comando ao alvo
                    buffer += '/n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("User terminated")
            self.socket.close()
            sys.exit(0)

    def listen(self) -> None:
        # funciona como um mini servidor ouvindo as conexões
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print("CLIENTE")
        while True:
            client_socket, addr = self.socket.accept()  # socket e endereço, para manter a conexão

            thread_client = threading.Thread(target=self.handle, args=(client_socket, ))
            thread_client.start()

    def handle(self, client_socket) -> None:
        # contém a lógica de upload, execução e shell interativo, etc
        if self.args.execute:  # executa comando
            output: str = execute(self.args.execute)
        elif self.args.upload:  # upload
            file: bytes = b''
            while True:
                data = socket.socket.recv(4096)
                if data:
                    file += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file)
            client_socket.send(f'Saved file {self.args.upload}'.encode())

        elif self.args.command: # shell interativo
            command: bytes = b''
            while True:
                try:
                    client_socket.send(b'#> ')
                    while '\n' not in command.decode():
                        command += client_socket.recv(64)
                    response = execute(command.decode())
                    command = b''
                except Exception as e:
                    print(f"Server was dead {e}")
                    self.socket.close()
                    sys.exit(0)




