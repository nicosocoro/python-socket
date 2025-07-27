# Socket Server Example

A hands-on demonstration of socket programming in Python, showcasing both TCP and Unix domain socket implementations.

## Key Concepts

### Socket
A socket is an endpoint for network communication between processes. It acts as an interface between the application layer and the transport layer of the network stack. Sockets can be used for both local (inter-process) and network communication.

### Socket Address Family
Defines the addressing scheme and protocol family used by the socket:

- **AF_INET**: IPv4 Internet protocols (TCP/UDP over IPv4)
- **AF_UNIX**: Local communication (Unix domain sockets)

### Unix Domain Sockets (.sock files)
Unix domain sockets use the file system as their address namespace.

### File Descriptor
A integer that serves as an index into the kernel's file descriptor table.

## Overview

This project demonstrates how to create a simple HTTP server using different socket types:
- **TCP Sockets**: Network-based communication using IP addresses and ports
- **Unix Domain Sockets**: File-based communication using socket files

## Features

- Simple HTTP server that responds to GET requests
- Support for both TCP and Unix domain sockets
- Graceful shutdown handling with signal management
- Clean socket file management for Unix domain sockets
- Basic HTTP request parsing and response generation

## Project Structure

```
local_server/
├── server.py      # HTTP server implementation
├── request.py     # HTTP client for testing
```

## Usage

### Starting the Server

Run the server with either TCP or Unix domain socket:

```bash
# Start with TCP socket (listens on localhost:8080)
python3 server.py --socket tcp

# Start with Unix domain socket (uses /tmp/local_server.sock)
python3 server.py --socket unix
```

### Making Requests

Use the client to test the server:

```bash
# Test TCP server
python3 request.py --socket tcp

# Test Unix domain socket server
python3 request.py --socket unix
```

### Important Notes

- The `--socket` parameter must match between client and server
- TCP server binds to `localhost:8080`
- Unix domain socket uses `/tmp/local_server.sock`
- Server responds with "running" for GET requests
- Other HTTP methods return "Method not allowed"

## How It Works

### TCP Sockets
- Uses `AF_INET` address family
- Binds to `localhost:8080`
- Accepts connections from any client that can reach the port
- Returns client address as `(host, port)` tuple

### Unix Domain Sockets
- Uses `AF_UNIX` address family
- Binds to socket file `/tmp/local_server.sock`
- Only accessible from the same machine
- Returns empty string for client address
- Automatically cleans up socket file on shutdown

## Example Output

### Server (TCP)
```
✅ Server running. File descriptor: 3
📨 New TCP connection from: ('127.0.0.1', 54321)
```

### Server (Unix)
```
✅ Server running. File descriptor: 3
📨 New Unix domain socket connection
```

### Client Response
```
args:Namespace(socket='tcp')
[+] Response: HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 7
Connection: close

running
```

## Signal Handling

The server gracefully handles shutdown signals:
- `SIGINT` (Ctrl+C)
- `SIGTERM`

When terminated, it:
1. Closes the server socket
2. Cleans up Unix socket file (if applicable)
3. Exits cleanly

## Error Handling

- Socket creation failures are caught and reported
- Invalid socket types raise descriptive exceptions
- Connection errors are handled gracefully
- Socket file cleanup on startup and shutdown

## Development Notes

This is a learning example demonstrating:
- Basic socket programming concepts
- HTTP request/response handling
- Different socket types and their characteristics
- Proper resource cleanup and signal handling