import tkinter as tk
import socket

from Client import AddClient
from Client.LoginFrame import LoginFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("Cyber Project")
        self.socket = socket.socket()
        self.PORT = 8000
        self.socket.connect(('127.0.0.1', self.PORT))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        add_frame = AddClient.AddClientFrame(master=container, controller=self)
        add_frame.grid(row=0, column=0, sticky="nsew")

        login_frame = LoginFrame(master=container, controller=self)
        login_frame.grid(row=0, column=0, sticky="nsew")

        self.frames["Login"] = login_frame
        self.frames["Add"] = add_frame

        self.show_frame("Login")

        self.mainloop()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_socket(self):
        return self.socket

if __name__ == '__main__':
    app = App()
