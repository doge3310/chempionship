import tkinter as tk
from peewee_model import User


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.text = tk.Text()
        self.text.pack()

        self.button = tk.Button(
            text="сделать заебись",
            command=self.view
        )
        self.button.pack()

    def view(self):
        for item in User.select():
            self.text.insert(tk.END, (item.id, item.username, item.password, "\n"))


root = tk.Tk()
root.geometry("500x500")
root.resizable(False, False)
myapp = App(root)
myapp.mainloop()
