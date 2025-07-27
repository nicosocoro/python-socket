import socket
import os
import signal
import sys
import argparse

def cleanup_socket(unix_socket_path):
    """Remove socket file if it exists"""
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

unix_socket_path = "/tmp/local_server.sock"

def build_tcp_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 8080))
    return s

def build_unix_socket():
    cleanup_socket(unix_socket_path)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(unix_socket_path)
    return s

def main():
    parser = argparse.ArgumentParser(description="Basic Socket server example")
    parser.add_argument("--socket", required=True, choices=['tcp', 'unix'], help="Socket type")
    args = parser.parse_args()

    socket_type = args.socket

    try:
        if socket_type == "tcp":
            server_socket = build_tcp_socket()
        elif socket_type == "unix":
            server_socket = build_unix_socket()
        else:
            raise Exception(f"Invalid socket type: {socket_type}. Must be 'tcp' or 'unix'")
        
        server_socket.listen(5)
        print(f"✅ Server running. File descriptor: {server_socket.fileno()}")
        
        # Set up signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            print('\n🛑 Shutting down server...')
            server_socket.close()
            if socket_type == "unix":
                cleanup_socket(unix_socket_path)
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Accept connections
        while True:
            client_socket, address = server_socket.accept()
            if socket_type == "unix":
                print(f"📨 New Unix domain socket connection")
            else:
                print(f"📨 New TCP connection from: {address}")
            handle_request(client_socket)

    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        server_socket.close()
        cleanup_socket(unix_socket_path)

if __name__ == "__main__":
    main()
