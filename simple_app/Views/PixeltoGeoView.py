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
            None if not self.check_inputs() else self.process_func(pixel_file=csv_path, tiff_file=tiff_path,
                                                                  out_folder=out_folder,out_filename=out_filename)

    def check_inputs(self):
        if not self.tiff_var.get():
            messagebox.showwarning("Input Error", "Please enter path to tiff file.")
            return False
        if not self.csv_var.get():
            messagebox.showwarning("Input Error", "Please enter path to csv file.")
            return False
        if not self.outfolder_var.get():
            messagebox.showwarning("Input Error", "Please enter output folder.")
            return False
        if not self.outfile_var.get() or self.outfile_var.get() == self.outfile_placeholder:
            messagebox.showwarning("Input Error", "Please enter output file name.")
            return False
        return True

    def show_pixel_to_geo_inputs(self):

        self.outfile_placeholder = "Enter the name for the output shapefile"
        label_title = tk.Label(self.content_frame, text="Pixel to Geo Coordinate Conversion", font=("Arial", 16))
        frame_tiff = FileSelectorFrame(self.content_frame, "TIFF File:", [("TIFF files", "*.tif *.tiff")])
        frame_csv = FileSelectorFrame(self.content_frame, "CSV File:", [("CSV files", "*.csv")])
        frame_outfolder = FolderSelectorFrame(self.content_frame, "Output Folder:")
        entry_outfile = TextInputFrame(self.content_frame, "Output Filename ", self.outfile_placeholder)
        button_process = tk.Button(self.content_frame, text="Process", command=self.process)

        self.tiff_var = frame_tiff.path_var
        self.csv_var = frame_csv.path_var
        self.outfolder_var = frame_outfolder.path_var
        self.outfile_var = entry_outfile.text_var

        label_title.pack(pady=10)
        frame_tiff.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_csv.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        frame_outfolder.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        entry_outfile.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        button_process.pack(side=tk.TOP, pady=20)