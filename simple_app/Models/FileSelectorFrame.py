import tkinter as tk
from tkinter import filedialog, messagebox


class FileSelectorFrame(tk.Frame):
    def __init__(self, master, label_text, filetypes, callback = None,btn_text="Process"):
        super().__init__(master)
        self.filetypes = filetypes
        self.callback = callback
        self.path_var = tk.StringVar()
        tk.Label(self, text=label_text).pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(self, textvariable=self.path_var, width=30)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.columnconfigure(1, weight=1)
        tk.Button(self, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        if self.callback is not  None:
            tk.Button(self, text=btn_text, command=self.callback).pack(side=tk.LEFT, padx=5)

    def get_value(self):
        return self.path_var.get()

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.path_var.set(path)