import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# List to store connected clients
clients = []


# Function to handle incoming client connections
def handle_client(client_socket):
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')

            # Broadcast the message to all connected clients
            for client in clients:
                client.send(bytes(message, 'utf-8'))

    except Exception as e:
        print(f"Error: {e}")
        clients.remove(client_socket)
        client_socket.close()


# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

# Accept and handle client connections
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
