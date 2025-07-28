import socket
import app_args
import socket_utils

def set_socket_timeout(socket):
    socket.settimeout(1)

def build_unix_socket():
    def builder():
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        set_socket_timeout(s)
        s.connect(socket_utils.SOCKET_PATH)
        return s
    return build_socket(builder)

def build_tcp_socket():
    def builder():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        set_socket_timeout(s)
        s.connect(("localhost", 8080))
        return s
    return build_socket(builder)

def build_socket(socket_builder):
    try:
        return socket_builder()
    except socket.error as e:
        print(f"[-] Socket error: {e}")
        return None

def get_socket(socket_type):
    if socket_type == socket_utils.TCP:
        return build_tcp_socket()
    if socket_type == socket_utils.UNIX:
        return build_unix_socket()
    else:
        raise Exception(f"Invalid socket type: {socket_type}. Must be '{socket_utils.TCP}' or '{socket_utils.UNIX}'")


def main():
    args = app_args.get_args()
    with get_socket(args.socket) as s:
        if s:
            s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            response = s.recv(1024)
            print(f"[+] Response: {response.decode()}")

if __name__ == "__main__":
    main()