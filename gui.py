# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
from main import *
import os.path


class ParserGui:
    def __init__(self, master):
        self.l_link = Label(master, width=20, text='URL')
        self.e_link = Entry(master, width=50)
        self.b_folder = Button(master, width=20, text="Folder", command=self.folder)
        self.e_folder = Entry(master, width=50)
        self.b_start = Button(master, width=20, text='Start', command=self.start)
        self.content_type = IntVar()
        self.type_pics = Radiobutton(master, text="pics", variable=self.content_type, value=1, width=10)
        self.type_vids = Radiobutton(master, text="vids", variable=self.content_type, value=2, width=10)
        self.type_all = Radiobutton(master, text="all", variable=self.content_type, value=3, width=10)
        self.status = Label(width=10, text="Status:")
        self.status_message = Label(width=20)
        self.l_link.grid(row=0, columnspan=3, padx=5, pady=5)
        self.e_link.grid(row=1, columnspan=3, padx=5, pady=5)
        self.b_folder.grid(row=2, columnspan=3, padx=5, pady=5)
        self.e_folder.grid(row=3, columnspan=3, padx=5, pady=5)
        self.type_pics.grid(row=4, column=0, sticky=W + E)
        self.type_vids.grid(row=4, column=1, sticky=W)
        self.type_all.grid(row=4, column=2, sticky=W)
        self.b_start.grid(row=5, columnspan=3)
        self.status.grid(row=7, column=0, pady=5)
        self.status_message.grid(row=7, column=1, columnspan=2, sticky=W)
        self.handler = StatusHandler(self.status_message)

    def folder(self):
        folder = filedialog.askdirectory()
        self.e_folder.insert(0, folder)

    def get_url(self):
        url = self.e_link.get()
        return url

    def get_path(self):
        path = os.path.abspath(self.e_folder.get())
        return path

    def get_content_type(self):
        content_val = self.content_type.get()
        return content_val

    def start(self):
        content_type = self.get_content_type()
        if content_type is None:
            self.handler.message("Please select content")
        else:
            path = self.get_path()
            url = self.get_url()
            try:
                if content_type == 1:                                                             # If pics
                    MainActions.parse_page_thread(url, path, "pics", self.status_message)
                elif content_type == 2:                                                           # If videos
                    MainActions.parse_page_thread(url, path, "videos", self.status_message)
                elif content_type == 3:                                                           # If all
                    MainActions.parse_page_thread(url, path, "all", self.status_message)

            except Exception:
                self.handler.message("Error")


if __name__ == "__main__":
    root = Tk()
    base = ParserGui(root)
    root.mainloop()
