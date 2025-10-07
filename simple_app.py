import tkinter as tk
from tkinter import filedialog, messagebox

from simple_app.Views.GeotoPixelView import GeoPixelView
from simple_app.Views.PixeltoGeoView import PixeltoGeoView



class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Geo/Pixel Coordinate Converter")
        self.root.geometry("400x250")

        menu_label = tk.Label(self.root, text="Choose an action:", font=("Arial", 14))
        menu_label.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, pady=5)

        self.content_frame = tk.Frame(self.root)
        self.view_gtp = GeoPixelView(self.content_frame)
        self.view_ptg = PixeltoGeoView(self.content_frame)

        btn_geo_to_pixel = tk.Button(button_frame, text="Convert Geo to Pixel Coordinates", width=30, command=self.show_geo_to_pixel_inputs)
        btn_pixel_to_geo = tk.Button(button_frame, text="Convert Pixel to Geo Coordinates", width=30, command=self.show_pixel_to_geo_inputs)

        btn_geo_to_pixel.pack(side=tk.TOP, pady=5)
        btn_pixel_to_geo.pack(side=tk.TOP, pady=5)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def run(self):
        self.root.mainloop()

    def show_geo_to_pixel_inputs(self):
        self.clear_content()
        process_type = 'geo_to_pixel'
        self.root.geometry("600x400")
        self.view_gtp.show_geo_to_pixel_inputs()
    

    def show_pixel_to_geo_inputs(self):
        self.clear_content()
        process_type = 'pixel_to_geo'
        self.root.geometry("600x400")
        self.view_ptg.show_pixel_to_geo_inputs()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()