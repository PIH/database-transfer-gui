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

MSG_APP_NAME = "Exportar Baso de Datos"
MSG_NEXT = "Siguiente"
MSG_DONE = "Ya!"
MSG_PASSWORD = "Contraseña"

MSG_EXPORT_PASSWORD = "Por favor, ingresa la contraseña de usuario “root” de MySQL. También necesitamos la contraseña para cifrar el archivo."
MSG_EXPORT_DATABASE_SELECT = "Selecciona la base de datos para exportar."
MSG_EXPORT_SAVE_FILE = "Elige un lugar para guardar el archivo."


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


class MainApplication(object):
    def __init__(self, parent):

        self.parent = parent
        self.step = 0
        self.password = None
        self.database = None
        self.filename = None

        self.parent.withdraw()
        self._do_step()

    def _do_step(self):
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

    def _go_to_next_step(self):
        debug("go_to_next_step")
        self.step += 1
        self._do_step()

    def _get_new_frame(self, title=MSG_APP_NAME):
        frame = tk.Toplevel(self.parent)
        frame.geometry("600x400")
        return frame

    def get_password(self):
        # Get password
        self.password = tkinter.simpledialog.askstring(
            MSG_PASSWORD, MSG_EXPORT_PASSWORD, show="*"
        )
        self._go_to_next_step()

    def select_database(self):
        debug("select_database")
        databases = get_database_list(self.password)

        frame = self._get_new_frame()

        w = tk.Label(frame, text=MSG_EXPORT_DATABASE_SELECT)
        w.pack()

        database_choice = tk.StringVar(frame)
        database_choice.set(databases[0])  # default value
        w = tk.OptionMenu(frame, database_choice, *databases)
        w.pack()

        def set_database():
            self.database = database_choice.get()
            frame.destroy()
            self._go_to_next_step()

        button = tk.Button(frame, text="OK", command=set_database)
        button.pack()

    def select_file(self):
        home = str(Path.home())
        self.filename = tkinter.filedialog.asksaveasfilename(
            initialdir=home,
            initialfile="openmrs-dump",
            title=MSG_EXPORT_SAVE_FILE,
            defaultextension=".zip",
            filetypes=(("zip file", "*.zip"),),
        )
        self._go_to_next_step()

    def execute(self):
        debug("execute")
        debug(self.password)
        debug(self.database)
        debug(self.filename)

        frame = self._get_new_frame()

        w = tk.Label(frame, text="Dumping...")
        w.pack()
        frame.update()

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

        w = tk.Label(frame, text="Zipping...")
        w.pack()
        frame.update()

        gzipcmd = "gzip -c " + sql_path + "> " + self.filename
        os.system(gzipcmd)

        w = tk.Label(frame, text=MSG_DONE)
        w.pack()

        button = tk.Button(frame, text="OK", command=self._go_to_next_step)
        button.pack()


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
    MainApplication(root)
    root.mainloop()
