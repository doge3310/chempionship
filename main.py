import tkinter as tk
from peewee_model import User
from tkinter import ttk


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        columns = ["1", "2", "3"]
        self.treeview = ttk.Treeview(columns=columns, show="headings")
        self.treeview.heading("1", text="id")
        self.treeview.heading("2", text="username")
        self.treeview.heading("3", text="password")
        self.treeview.column("1", width=30, anchor="center")
        self.treeview.column("2", width=100, anchor="center")
        self.treeview.column("3", width=350, anchor="center")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # self.username = tk.Entry()
        # self.password.pack()

        # self.password = tk.Entry()
        # self.password.pack()

        self.button = tk.Button(
            text="сделать заебись",
            command=self.view
        )
        self.button.pack()

    def view(self):
        for item in User.select():
            self.treeview.insert("", 0, values=[item.id, item.username, item.password])


root = tk.Tk()
root.geometry("500x500")
myapp = App(root)
myapp.mainloop()
