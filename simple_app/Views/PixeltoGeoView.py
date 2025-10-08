import tkinter as tk
from tkinter import filedialog, messagebox
from simple_app.Models.FileSelectorFrame import FileSelectorFrame
from simple_app.Models.FolderSelectorFrame import FolderSelectorFrame
from simple_app.Models.TextInputFrame import TextInputFrame
from simple_app.functions.pixel_to_geo import pixel_to_geo

class PixeltoGeoView:
    def __init__(self, master):
        self.content_frame = master
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.process_func = pixel_to_geo

    def process(self):
        if self.process_func is not None:
            tiff_path = self.tiff_var.get()
            csv_path = self.csv_var.get()
            out_folder = self.outfolder_var.get()
            out_filename = self.outfile_var.get()
            if not tiff_path or not csv_path or not out_folder or not out_filename:
                messagebox.showwarning("Input Error", "Please enter all required fields.")
                return
            self.process_func(tiff_path, csv_path,out_folder,out_filename)

    def show_pixel_to_geo_inputs(self):


        frame_tiff = FileSelectorFrame(self.content_frame, "TIFF File:", [("TIFF files", "*.tif;*.tiff")])
        frame_csv = FileSelectorFrame(self.content_frame, "CSV File:", [("CSV files", "*.csv")])
        frame_outfolder = FolderSelectorFrame(self.content_frame, "Output Folder:")
        entry_outfile = TextInputFrame(self.content_frame, "Output Filename ", "Enter the name for the output shapefile")
        button_process = tk.Button(self.content_frame, text="Process", command=self.process)

        self.tiff_var = frame_tiff.path_var
        self.csv_var = frame_csv.path_var
        self.outfolder_var = frame_outfolder.path_var
        self.outfile_var = entry_outfile.text_var

        frame_tiff.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_csv.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_outfolder.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        entry_outfile.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        button_process.pack(side=tk.TOP, pady=20)