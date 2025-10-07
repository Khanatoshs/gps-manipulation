import tkinter as tk
from tkinter import filedialog, messagebox
from simple_app.Models.FileSelectorFrame import FileSelectorFrame
from simple_app.Models.FolderSelectorFrame import FolderSelectorFrame

class PixeltoGeoView:
    def __init__(self, master):
        self.content_frame = master
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.process_func = None

    def process(self):
        if self.process_func is not None:
            tiff_path = self.tiff_var.get()
            csv_path = self.csv_var.get()
            if not tiff_path or not csv_path:
                messagebox.showwarning("Input Error", "Please select both TIFF and CSV files.")
                return
            self.process_func(tiff_path, csv_path)

    def show_pixel_to_geo_inputs(self):


        frame_tiff = FileSelectorFrame(self.content_frame, "TIFF File:", [("TIFF files", "*.tif;*.tiff")])
        frame_csv = FileSelectorFrame(self.content_frame, "CSV File:", [("CSV files", "*.csv")])
        frame_outfolder = FolderSelectorFrame(self.content_frame, "Output Folder:")

        self.tiff_var = frame_tiff.path_var
        self.csv_var = frame_csv.path_var

        frame_tiff.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_csv.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_outfolder.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)