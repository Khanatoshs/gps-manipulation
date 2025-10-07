import tkinter as tk

class TextInputFrame(tk.Frame):
    def __init__(self, master, label_text, default_text=""):
        super().__init__(master)
        self.text_var = tk.StringVar(value=default_text)
        tk.Label(self, text=label_text).pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(self, textvariable=self.text_var, width=30)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.columnconfigure(1, weight=1)

    def get_value(self):
        return self.text_var.get()