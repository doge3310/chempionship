import tkinter as tk
from peewee_model import User, Roles, News, Comments
from hasher import hash, verify
from tkinter import ttk


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.tables = {User: ["id", "username", "password", "role_id"],
                       Roles: ["id", "name"],
                       News: ["id", "name", "author", "content"],
                       Comments: ["id", "name", "new_id", "content"]}

        self.tabs = [User, Roles, News, Comments]

        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.user_frame = ttk.Frame()
        self.role_frame = ttk.Frame()
        self.news_frame = ttk.Frame()
        self.comments_frame = ttk.Frame()

        self.user_frame.pack(expand=True, fill=tk.BOTH)
        self.role_frame.pack(expand=True, fill=tk.BOTH)
        self.news_frame.pack(expand=True, fill=tk.BOTH)
        self.comments_frame.pack(expand=True, fill=tk.BOTH)

        self.notebook.add(self.user_frame, text="user")
        self.notebook.add(self.role_frame, text="role")
        self.notebook.add(self.news_frame, text="news")
        self.notebook.add(self.comments_frame, text="comments")

        self.active = self.tabs[self.notebook.index(self.notebook.select())]

        self.label = ttk.Label()
        self.label.pack()

        self.instructions = ttk.Label(text=f"you need {self.tables[self.active]} parameters")
        self.instructions.pack()

        self.entry = ttk.Entry()
        self.entry.pack()

        self.db_view = tk.Button(
            text="db view",
            command=self.view_data
        )
        self.db_view.pack()

        self.reg = tk.Button(
            text="register",
            command=self.register_data
        )
        self.reg.pack()

        self.delete = tk.Button(
            text="delete",
            command=self.delete_data
        )
        self.delete.pack()

        self.change_user = tk.Button(
            text="change",
            command=self.change_data
        )
        self.change_user.pack()

        self.search_user = tk.Button(
            text="search",
            command=self.search_data
        )
        self.search_user.pack()

    def view_data(self):
        self.upd()

        lst = self.view(self.active)

        self.label.config(text=lst)

    def register_data(self):
        self.upd()

        self.regi(self.active)

    def delete_data(self):
        self.upd()

        self.dele(self.active)

    def change_data(self):
        self.upd()

        self.chan(self.active)

    def search_data(self):
        self.upd()

        self.label.config(text=self.search(self.active))


    def upd(self):
        self.active = self.tabs[self.notebook.index(self.notebook.select())]

    def view(self, model):
        lst = []

        for item in model.select():
            string = ""

            for jtem in self.tables[model]:
                out = getattr(item, jtem)

                string += " " + str(out)

            lst.append(string + "\n")

        return lst

    def regi(self, model):
        try:
            fields = self.entry.get().split("/")

            data = {item: fields[index] for index, item in enumerate(self.tables[model])}

            try:
                data["password"] = hash(data["password"])

            except KeyError:
                pass

            user, _ = model.get_or_create(**data)

            model.update()

        except IndexError:
            self.instructions.config(text=f"you need {self.tables[self.active]} parameters")

    def dele(self, model):
        self.instructions.config(text="you need id user")

        model.delete_by_id(self.entry.get())

    def chan(self, model):
        lst = self.tables[self.active][1:] + ["id_for_search"]
        self.instructions.config(text=f"you need {lst} parameters")
        vals = self.entry.get().split("/")

        try:
            if "password" in lst:
                vals[1] = hash(vals[1])

            table = model.get(model.id == vals[-1])

            for index, item in enumerate(lst[: -1]):
                setattr(table, item, vals[index])

            table.save()

        except:
            self.instructions.config(text=f"you need {lst} parameters")

    def search(self, model):
        self.instructions.config(text="you need name user")
        table = self.tables[model]
        name = self.entry.get()
        lst = []

        for item in model.select():
            rec = getattr(item, table[1])

            if name in str(rec):
                string = ""

                for jtem in table:
                    out = getattr(item, jtem)

                    string += " " + str(out)

                lst.append(string + "\n")

        return lst


root = tk.Tk()
root.geometry("500x500")
root.resizable(False, False)
myapp = App(root)
myapp.mainloop()
