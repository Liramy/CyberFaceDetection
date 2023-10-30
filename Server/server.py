import io
import pickle

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


def receive_user(c: socket.socket):
    received_data = c.recv(4096)

    # Convert the data from bytes to readable data using pickle
    data = pickle.loads(received_data)

    # Access the type of interaction chosen
    if data['interaction'] == 'Add User':
        image = data['image']
        username = data['username']
        password = data['password']

        create_user(username=username, password=password, image=image)

    else:
        # TODO: Send login info and image
        pass


def create_user(username, password, image):
    with open('../Server/Users.txt', 'r') as file:
        file_data = file.read()

    with open('../Server/Users.txt', 'w') as file:
        file.write(f"{file_data}\n{username}-:-{password}")

    with open(f'../Server/Users_face/{username}.png', 'wb') as file:
        file.write(image)


def create_dir():
    users_exists = os.path.exists('../Server/Users.txt')
    if not users_exists:
        with open('../Server/Users.txt', 'w') as file:
            pass

    users_exists = os.path.exists('../Server/Users_face')
    if not users_exists:
        os.makedirs('../Server/Users_face')


def load_image(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = '127.0.0.1'
PORT = 8000

create_dir()

client_dict: {any: socket.socket} = {}
client_interaction: {socket.socket: int} = {}

server_socket.bind((IP, PORT))

server_socket.listen(5)

while True:
    client_socket, client_addr = server_socket.accept()
    client_dict[client_addr] = client_socket

    threading.Thread(
        target=receive_user,
        args=(client_socket,)
    ).start()
