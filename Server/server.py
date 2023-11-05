import io
import pickle

import select
import socket
import threading
import os

from PIL import Image


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
        input_username = data['username']

        with open('Users.txt', 'r') as file:
            users_data = file.readlines()

        is_exists = False
        user = {
            'exists': is_exists
        }

        for user_data in users_data:
            username, password = user_data.split('-:-')
            if username == input_username:
                try:
                    with open(f'Users_face/{username}.png', 'rb') as image:
                        image_data = image.read()

                except NameError:
                    with open(f'Users_face/{username}.jpg', 'rb') as image:
                        image_data = image.read()

                is_exists = True

                user = {
                    'image': image_data,
                    'username': username,
                    'password': password,
                    'exists': is_exists
                }

                serialized_data = pickle.dumps(user)

                c.sendall(serialized_data)
                break
        if not is_exists:
            c.sendall(pickle.dumps(user))
        else:
            c.sendall(pickle.dumps(user))


def create_user(username, password, image):
    with open('Users.txt', 'r') as file:
        file_data = file.read()

    with open('Users.txt', 'w') as file:
        file.write(f"{file_data}\n{username}-:-{password}")

    try:
        with open(f'Users_face/{username}.png', 'wb') as file:
            file.write(image)

    except NameError:
        with open(f'Users_face/{username}.jpg', 'wb') as file:
            file.write(image)


def create_dir():
    users_exists = os.path.exists('Users.txt')
    if not users_exists:
        with open('Users.txt', 'w') as file:
            pass

    users_exists = os.path.exists('Users_face')
    if not users_exists:
        os.makedirs('Users_face')


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
