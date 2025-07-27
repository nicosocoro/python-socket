import socket
import argparse

def build_unix_socket():
    def builder():
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(1) 
        s.connect("/tmp/local_server.sock")
        return s
    return build_socket(builder)

def build_tcp_socket():
    def builder():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) 
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
    if socket_type == "tcp":
        return build_tcp_socket()
    if socket_type == "unix":
        return build_unix_socket()
    else:
        raise Exception(f"Invalid socket type: {socket_type}. Must be 'tcp' or 'unix'")

parser = argparse.ArgumentParser(description="Basic Socket client example")
parser.add_argument("--socket", required=True, choices=['tcp', 'unix'], help="Socket type")
args = parser.parse_args()
print(f"arsgs:{args}")
with get_socket(args.socket) as s:
    if s:
        s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        response = s.recv(1024)
        print(f"[+] Response: {response.decode()}")