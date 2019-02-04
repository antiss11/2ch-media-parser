# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
from main import *
import os.path


class Parser:
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
        self.status = Label(width=5)
        self.l_link.grid(row=0, columnspan=3, padx=5, pady=5)
        self.e_link.grid(row=1, columnspan=3, padx=5, pady=5)
        self.b_folder.grid(row=2, columnspan=3, padx=5, pady=5)
        self.e_folder.grid(row=3, columnspan=3, padx=5, pady=5)
        self.type_pics.grid(row=4, column=0, sticky=W + E)
        self.type_vids.grid(row=4, column=1, sticky=W)
        self.type_all.grid(row=4, column=2, sticky=W)
        self.b_start.grid(row=5, columnspan=3)
        self.status.grid(row=7, column=0, sticky=W)

    def folder(self):
        folder = filedialog.askdirectory()
        self.e_folder.insert(0, folder)

    def get_url(self):
        self.url = self.e_link.get()

    def get_path(self):
        self.path = os.path.abspath(self.e_folder.get())

    def get_content_type(self):
        self.content_val = self.content_type.get()

    def start(self):
        try:
            self.get_content_type()
            self.get_path()
            self.get_url()
            if self.content_val == 1:                           # If pics
                parse_page(self.url, self.path, 'pics')
            elif self.content_val == 2:                         # If videos
                parse_page(self.url, self.path, 'videos')
            elif self.content_val == 3:                         # If all
                parse_page(self.url, self.path, 'all')
                self.status['text'] = 'Ok!'
        except Exception:
            self.status['text'] = 'Error'


if __name__ == "__main__":
    root = Tk()
    base = Parser(root)
    root.mainloop()
