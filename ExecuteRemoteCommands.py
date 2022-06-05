import shlex
import subprocess


def execute(*args) -> None or str:
    # executa um programa no sistema local e retorna a saida como texto
    command: str = args[0].strip()
    output: bytes = b''
    if not command:
        return None
    try:
        output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
        return output.decode()
    except UnicodeDecodeError:
        ...
    finally:
        return output.decode()


if __name__ == '__main__':
    execute("ping 1.1.1.1")
