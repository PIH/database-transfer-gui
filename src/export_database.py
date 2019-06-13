import os
from pathlib import Path
import tempfile

import mysql.connector
import tkinter as tk
import tkinter.simpledialog
import tkinter.filedialog


DEBUG = False
DB_HOST = "localhost"
DB_USER = "root"


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.step = 0
        self.password = None
        self.database = None
        self.filename = None

        self.do_step()

    def do_step(self):
        debug("do_step on step {}".format(self.step))
        if self.step == 0:
            self.get_password()
        elif self.step == 1:
            self.select_database()
        elif self.step == 2:
            self.select_file()
        elif self.step == 3:
            self.execute()
        elif self.step == 4:
            self.parent.destroy()
        else:
            raise Exception(
                "Somehow wound up on non-existant step {}".format(self.step)
            )

    def go_to_next_step(self):
        debug("go_to_next_step")
        self.step += 1
        self.do_step()

    def get_password(self):
        # Get password
        self.parent.withdraw()
        self.password = tkinter.simpledialog.askstring(
            "Password", "Enter password:", show="*"
        )
        self.go_to_next_step()

    def select_database(self):
        debug("select_database")
        self.parent.deiconify()
        databases = get_database_list(self.password)
        database_choice = tk.StringVar(self.parent)
        database_choice.set(databases[0])  # default value
        w = tk.OptionMenu(self.parent, database_choice, *databases)
        w.pack()

        def set_database():
            self.database = database_choice.get()
            self.parent.withdraw()
            self.go_to_next_step()

        button = tk.Button(self.parent, text="OK", command=set_database)
        button.pack()

    def select_file(self):
        home = str(Path.home())
        self.filename = tkinter.filedialog.asksaveasfilename(
            initialdir=home,
            initialfile="openmrs-dump",
            title="Select save file",
            defaultextension=".zip",
            filetypes=(("zip file", "*.zip"),),
        )
        self.go_to_next_step()

    def execute(self):
        debug("execute")
        print(self.password)
        print(self.database)
        print(self.filename)
        print("Dumping...")
        temp_dir = tempfile.TemporaryDirectory()
        sql_path = str(Path(temp_dir.name) / (self.database + ".sql"))
        dumpcmd = (
            "mysqldump -h "
            + DB_HOST
            + " -u "
            + DB_USER
            + " -p'"
            + self.password
            + "' "
            + self.database
            + " > "
            + sql_path
        )
        os.system(dumpcmd)
        print("Zipping...")
        gzipcmd = "gzip -c " + sql_path + "> " + self.filename
        os.system(gzipcmd)
        print("Done!")
        self.go_to_next_step()


def get_database_list(mysql_parent_password):
    conn = mysql.connector.connect(
        user="root", password=mysql_parent_password, host="localhost", buffered=True
    )
    cursor = conn.cursor()
    cursor.execute(("show databases"))
    databases = [d[0] for d in cursor]
    return databases


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
