import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfile


class LoginFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.username = StringVar()
        self.password = StringVar()
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

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

        add_switch_button = Button(
            master=self, text="Add client", font=("Arial", 15), command=lambda: controller.show_frame("Add"))
        add_switch_button.grid(row=0, column=0, sticky="w", pady=70, padx=80)
