import socket
import os
import signal
import sys
import argparse
import app_args
import socket_utils

def cleanup_unix_socket():
    """Remove socket file if it exists"""
    unix_socket_path = socket_utils.SOCKET_PATH
    if os.path.exists(unix_socket_path):
        os.unlink(unix_socket_path)
        print(f"Removed existing socket: {unix_socket_path}")

def handle_request(client_socket):
    """Handle incoming HTTP request"""
    try:
        # Receive request
        request = client_socket.recv(1024).decode('utf-8')
        
        # Simple request parsing
        if request.startswith('GET'):
            # Send HTTP response
            response = """HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 7
Connection: close

running"""
            client_socket.send(response.encode('utf-8'))
        else:
            # Method not allowed
            response = """HTTP/1.1 405 Method Not Allowed
Content-Type: text/plain
Content-Length: 18
Connection: close

Method not allowed"""
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

def build_tcp_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 8080))
    return s

def build_unix_socket():
    cleanup_unix_socket()
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(socket_utils.SOCKET_PATH)
    return s

def main():
    args = app_args.get_args()
    socket_type = args.socket

    try:
        if socket_type == socket_utils.TCP:
            server_socket = build_tcp_socket()
        elif socket_type == socket_utils.UNIX:
            server_socket = build_unix_socket()
        else:
            raise Exception(f"Invalid socket type: {socket_type}. Must be '{socket_utils.TCP}' or '{socket_utils.UNIX}'")
        
        server_socket.listen(5)
        print(f"✅ Server running. File descriptor: {server_socket.fileno()}")
        
        # Set up signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            print('\n🛑 Shutting down server...')
            server_socket.close()
            if socket_type == socket_utils.UNIX:
                cleanup_unix_socket()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Accept connections
        while True:
            client_socket, address = server_socket.accept()
            if socket_type == socket_utils.UNIX:
                print(f"📨 New Unix domain socket connection")
            else:
                print(f"📨 New TCP connection from: {address}")
            handle_request(client_socket)

    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        server_socket.close()
        cleanup_unix_socket()

if __name__ == "__main__":
    main()
