import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

# Function to handle receiving messages
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            msg_listbox.insert(tk.END, message)
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to send messages
def send(event=None):
    message = my_msg.get()
    my_msg.set("")  # Clear the input field
    client_socket.send(bytes(message, 'utf-8'))
    if message == "/quit":
        client_socket.close()
        top.quit()

# Create the main GUI window
top = tk.Tk()
top.title("Chat Application")

# Create and configure the message listbox
msg_listbox = scrolledtext.ScrolledText(top, wrap=tk.WORD)
msg_listbox.pack(expand=True, fill=tk.BOTH)

# Create the input field and send button
my_msg = tk.StringVar()
entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(expand=True, fill=tk.X)
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Start a thread to handle receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start the Tkinter main loop
top.protocol("WM_DELETE_WINDOW", client_socket.close)
tk.mainloop()
