import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
from cv2 import *
import random

from Client import AddClient
from Client.LoginFrame import LoginFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("Cyber Project")

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


if __name__ == '__main__':
    app = App()
