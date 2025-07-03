import os
import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

# Your Unsplash access key (export before running, or hardcode here)
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
if not UNSPLASH_ACCESS_KEY:
    raise Exception("Please set your UNSPLASH_ACCESS_KEY environment variable.")

class ImageGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Generator with Dropdown & Search")
        self.geometry("850x650")
        
        # Categories for dropdown
        self.categories = ["Nature", "Mountains", "Cats", "Dogs", "City", "Flowers", "Beach", "Food", "Space", "Anime", "Custom"]
        self.current_images = []
        self.current_index = 0
        
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # Dropdown
        self.category_var = tk.StringVar(value=self.categories[0])
        ttk.Label(frame, text="Select Category:").grid(row=0, column=0, padx=5)
        self.dropdown = ttk.Combobox(frame, textvariable=self.category_var, values=self.categories, state="readonly")
        self.dropdown.grid(row=0, column=1, padx=5)

        # Custom entry if 'Custom' selected
        self.custom_var = tk.StringVar()
        self.custom_entry = ttk.Entry(frame, textvariable=self.custom_var, width=20)
        self.custom_entry.grid(row=0, column=2, padx=5)
        self.custom_entry.insert(0, "Optional keyword")

        ttk.Button(frame, text="Search", command=self.search_images).grid(row=0, column=3, padx=5)
        ttk.Button(frame, text="Next", command=self.show_next_image).grid(row=0, column=4, padx=5)
        ttk.Button(frame, text="Download", command=self.download_image).grid(row=0, column=5, padx=5)

        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=15)

    def search_images(self):
        query = self.category_var.get()
        if query == "Custom":
            query = self.custom_var.get().strip()
            if not query:
                messagebox.showwarning("Input error", "Please enter a keyword for Custom category.")
                return

        try:
            self.current_images = self.fetch_images(query)
            self.current_index = 0
            if not self.current_images:
                messagebox.showinfo("No Results", "No images found for this query.")
                return
            self.show_image(self.current_images[self.current_index])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_images(self, query):
        url = "https://api.unsplash.com/search/photos"
        params = {"client_id": UNSPLASH_ACCESS_KEY, "query": query, "per_page": 10}
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return [item["urls"]["regular"] for item in data.get("results", [])]

    def show_image(self, img_url):
        resp = requests.get(img_url)
        img = Image.open(BytesIO(resp.content))
        img.thumbnail((800, 500))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)
        self.current_image_url = img_url

    def show_next_image(self):
        if not self.current_images:
            messagebox.showinfo("No images", "Perform a search first.")
            return
        self.current_index = (self.current_index + 1) % len(self.current_images)
        self.show_image(self.current_images[self.current_index])

    def download_image(self):
        if not hasattr(self, 'current_image_url') or not self.current_image_url:
            messagebox.showinfo("No image", "Generate or search an image first.")
            return
        try:
            resp = requests.get(self.current_image_url)
            query = self.category_var.get()
            if query == "Custom":
                query = self.custom_var.get().strip()
            filename = f"{query}_{self.current_index + 1}.jpg"
            with open(filename, "wb") as f:
                f.write(resp.content)
            messagebox.showinfo("Saved", f"Image saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ImageGeneratorApp()
    app.mainloop()
