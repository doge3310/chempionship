import tkinter as tk
from peewee_model import User
from hasher import hash, verify
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

        self.db_view = tk.Button(
            text="db view",
            command=self.view
        )
        self.db_view.pack()

        self.username = tk.Entry()
        self.username.pack()

        self.password = tk.Entry()
        self.password.pack()

        self.reg = tk.Button(
            text="register",
            command=self.register
        )
        self.reg.pack()

        self.delete = tk.Button(
            text="delete",
            command=self.delete_user
        )
        self.delete.pack()

        self.newuser_name = tk.Entry()
        self.newuser_name.pack()

        self.new_name = tk.Entry()
        self.new_name.pack()

        self.newuser_password = tk.Entry()
        self.newuser_password.pack()

        self.change_user = tk.Button(
            text="change",
            command=self.change
        )
        self.change_user.pack()

    def view(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for item in User.select():
            self.treeview.insert("", 0, values=[item.id, item.username, item.password])

    def register(self):
        User.get_or_create(username=self.username.get(),
                           defaults={
                               "password": hash(self.password.get())
                           })

    def delete_user(self):
        for select_user in self.treeview.selection():
            item = self.treeview.item(select_user)
            username = item["values"]
            user = User.get(username=username[1])
            User.delete_by_id(user)

    def change(self):
        username = self.newuser_name.get()
        user = User.get(User.username == username)

        user.username = self.new_name.get()
        user.password = hash(self.newuser_password.get())

        user.save()


root = tk.Tk()
root.geometry("500x500")
root.resizable(False, False)
myapp = App(root)
myapp.mainloop()
