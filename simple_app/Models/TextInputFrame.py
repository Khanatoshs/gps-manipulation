import tkinter as tk

class TextInputFrame(tk.Frame):
    def __init__(self, master, label_text, default_text="Insert text here"):
        super().__init__(master)
        self.placeholder = default_text
        self.text_var = tk.StringVar(value="")
        tk.Label(self, text=label_text).pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(self, textvariable=self.text_var, width=30)
        self.entry.insert(0, default_text)
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)

        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.columnconfigure(1, weight=1)

    def on_focus_in(self,event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg="black") # Optional: change text color to normal
    def on_focus_out(self,event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="gray") # Optional: change text color to gray

    def get_value(self):
        return self.text_var.get()