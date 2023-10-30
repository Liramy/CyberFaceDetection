import os.path
import pickle
import socket
import tkinter
import ImageEncyption
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class AddClientFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.username = StringVar()
        self.password = StringVar()
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.image = None
        self.image_path = None
        self.key = None

        login_label = ttk.Label(self, text="Log In", font=("Arial", 30))
        login_label.grid(row=0, column=1, columnspan=2, sticky="news", pady=40, padx=240)

        username_label = ttk.Label(self, text='Username:', font=("Arial", 15))
        username_label.grid(row=1, column=1, columnspan=1, sticky="news", pady=40)

        username_textbox = ttk.Entry(self, textvariable=self.username, font=("Arial", 15))
        username_textbox.grid(row=1, column=2, columnspan=1, pady=40)

        password_label = ttk.Label(self, text='Password:', font=("Arial", 15))
        password_label.grid(row=2, column=1, columnspan=1, sticky="news", pady=40)

        password_textbox = ttk.Entry(self, textvariable=self.password, font=("Arial", 15))
        password_textbox.grid(row=2, column=2, columnspan=1, pady=40)

        image_pick_button = Button(self, text="Upload Image", command=lambda: self.upload_image(), font=("Arial", 15))
        image_pick_button.grid(row=3, column=1, columnspan=1, pady=40)

        login_switch_button = Button(
            master=self, text="Log In", font=("Arial", 15), command=lambda: controller.show_frame("Login"))
        login_switch_button.grid(row=0, column=0, sticky="w", pady=80, padx=80)

        save_button = Button(
            master=self, text="Save Client", font=("Arial", 15),
            command=lambda: self.save_client(controller.get_socket())
        )
        save_button.grid(row=4, column=1, pady=40)

    def upload_image(self):
        i_types = [('Jpg Files', '*.jpg'),
                   ('PNG Files', '*.png')]

        filename = filedialog.askopenfilename(filetypes=i_types, multiple=True)
        self.image_path = filename[0]
        col = 2
        row = 3
        for f in filename:
            img = Image.open(f)
            img = img.resize((100, 100))
            self.image = img
            img = ImageTk.PhotoImage(img)
            e = ttk.Label(self)
            e.grid(row=row, column=col)
            e.image = img
            e['image'] = img
            if col == 3:
                row = row + 1
                col = 1
            else:
                col = col + 1

    def save_client(self, client_socket: socket.socket()):
        wanted_path = "../Client/Face"
        path_exists = os.path.exists(wanted_path)

        if not path_exists:
            os.makedirs(wanted_path)

        self.image.save(f"../Client/Face/{self.username.get()}.{self.image_path[-3:]}")

        self.key = ImageEncyption.encrypt_image(
            path=f"../Client/Face/{self.username.get()}.{self.image_path[-3:]}")

        file = open(f"../Client/Face/{self.username.get()}.{self.image_path[-3:]}", 'rb')
        image = file.read()
        file.close()

        # Deletes the image from existence
        os.remove(f"../Client/Face/{self.username.get()}.{self.image_path[-3:]}")

        # Dictionary with all data
        user_data = {
            'image': image,
            'interaction': 'Add User',
            'username': self.username.get(),
            'password': self.password.get()
        }

        user_data = pickle.dumps(user_data)
        self.controller.get_socket().sendall(user_data)
