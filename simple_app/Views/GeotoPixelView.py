import tkinter as tk
from tkinter import filedialog, messagebox
from simple_app.Models.TextInputFrame import TextInputFrame
from simple_app.Models.FileSelectorFrame import FileSelectorFrame
from simple_app.Models.FolderSelectorFrame import FolderSelectorFrame
from simple_app.functions.geo_to_pixel import geo_to_pixel

class GeoPixelView:
    def __init__(self, master):
        self.master = master
        self.content_frame = master
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.process_func = geo_to_pixel

    def process(self):
        if self.process_func is not None:
            tiff_path = self.tiff_var.get()
            csv_path = self.csv_var.get()
            out_folder = self.outfolder_var.get()
            out_filename = self.outfile_var.get()
            if not tiff_path or not csv_path or not out_folder or not out_filename:
                messagebox.showwarning("Input Error", "Please enter all required fields.")
                return
            self.process_func(csv_path, tiff_path,out_folder,out_filename)

    def show_geo_to_pixel_inputs(self):
        frame_tiff = FileSelectorFrame(self.content_frame, "TIFF File:", [("TIFF files", "*.tif;*.tiff")])
        frame_csv = FileSelectorFrame(self.content_frame, "CSV File:", [("CSV files", "*.csv")])
        frame_outfolder = FolderSelectorFrame(self.content_frame, "Output Folder:")
        entry_outfile = TextInputFrame(self.content_frame, "Output File Name:", "Enter the name for the output CSV")
        entry_category = TextInputFrame(self.content_frame, "Category:", "Enter the category of the points")
        button_process = tk.Button(self.content_frame, text="Process", command=self.process)

        self.tiff_var = frame_tiff.path_var
        self.csv_var = frame_csv.path_var
        self.outfolder_var = frame_outfolder.path_var
        self.outfile_var = entry_outfile.text_var
        self.category_var = entry_category.text_var

        frame_tiff.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_csv.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_outfolder.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        entry_outfile.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        entry_category.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        button_process.pack(side=tk.TOP, pady=20)

  