import io

import select
import socket
import threading
import os

from PIL import Image

"""
  Adding employees:
  - When someone enters your group in the client GUI menu press Add Employee.
  - In the new tab enter the name and password.
  - After that it will ask for a picture, make sure to give one where 
    the face is visible and clear.
  - Press 'Done' and you're done, a new employee was added.
"""

"""
  Start of operations:
  - The server initializes the loging in feature.
  - Client enters and gives a name that exists with the correct password,
    the check is done by encrypting the password and checking if the encrypted
    entered password is the same as the stored one.
  - Server checks and then sends the client the encrypted image of the employee.
  - Client does the decrypting with the user_key and checks if the faces match.
  - If they match the server accepts the client and gives confirmation.
"""


def on_new_client(client_socket: socket.socket, addr):
    print(f"connection established with {addr}")


def create_user(raw_data: bytes):
    raw_data = raw_data.decode()
    username, password = raw_data.split('/***-***/')

    file = open('../Server/Users.txt', 'r')
    file_data = file.read()
    file.close()

    file = open('../Server/Users.txt', 'w')
    file.write(file_data + f'{username}-:-{password}\n')
    file.close()


def create_dir():
    users_exists = os.path.exists('../Server/Users.txt')
    if not users_exists:
        os.makedirs('../Server/Users.txt')


def load_image(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = '127.0.0.1'
PORT = 8000

create_dir()

client_dict: {any: socket.socket} = {}
client_interaction: {socket.socket: int} = {}

server_socket.bind((IP, PORT))

server_socket.listen()

while True:
    client_socket, client_addr = server_socket.accept()
    client_dict[client_addr] = client_socket
    client_interaction[client_addr] = -1

    on_welcome = threading.Thread(target=on_new_client, args=(client_socket, client_addr,))
    on_welcome.start()

    rlist, wlist, _ = select.select([], [], [], __timeout=10)

    for readable in rlist:
        data = readable.recv(2048)
        readable_addr = readable.getsockname()

        # When interaction is -1, action is undecided
        if client_interaction[readable_addr] == -1:
            client_interaction[readable_addr] = data.decode()

        # When interaction is 0, action is adding a new user
        if client_interaction[readable_addr] == 1:
            add_user = threading.Thread(target=create_user, args=(data,))
            add_user.start()

        if client_interaction[readable_addr] == 2:
            pass
