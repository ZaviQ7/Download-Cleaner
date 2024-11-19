import os
import shutil
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog

class DownloadCleaner:
    def __init__(self):
        # Define common file type categories
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.csv'],
            'Audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'Video': ['.mp4', '.avi', '.mkv', '.mov'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Others': []  # For uncategorized files
        }
        
        self.create_gui()

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Download Folder Cleaner")
        self.window.geometry("400x300")

        # Folder selection
        self.folder_path = tk.StringVar()
        tk.Label(self.window, text="Select Download Folder:").pack(pady=10)
        tk.Entry(self.window, textvariable=self.folder_path, width=40).pack()
        tk.Button(self.window, text="Browse", command=self.browse_folder).pack(pady=5)

        # Action buttons
        tk.Button(self.window, text="Preview Changes", command=self.preview_changes).pack(pady=10)
        tk.Button(self.window, text="Clean Folder", command=self.clean_folder).pack(pady=5)

        self.window.mainloop()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        self.folder_path.set(folder)

    def get_category(self, file):
        ext = os.path.splitext(file)[1].lower()
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return 'Others'

    def preview_changes(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a folder first!")
            return

        changes = self.analyze_folder()
        preview_text = "Proposed Changes:\n\n"
        for category, files in changes.items():
            preview_text += f"{category}: {len(files)} files\n"
            for file in files[:3]:  # Show first 3 files as example
                preview_text += f"  - {file}\n"
            if len(files) > 3:
                preview_text += "  ...\n"

        messagebox.showinfo("Preview", preview_text)

    def analyze_folder(self):
        changes = {category: [] for category in self.categories.keys()}
        folder = self.folder_path.get()
        
        for file in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, file)):
                category = self.get_category(file)
                changes[category].append(file)
        
        return changes

    def clean_folder(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a folder first!")
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to organize the folder?"):
            return

        folder = self.folder_path.get()
        organized = 0

        for category in self.categories.keys():
            category_path = os.path.join(folder, category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                category = self.get_category(file)
                destination = os.path.join(folder, category, file)
                
                # Handle duplicate files
                if os.path.exists(destination):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(destination):
                        new_name = f"{base}_{counter}{ext}"
                        destination = os.path.join(folder, category, new_name)
                        counter += 1

                shutil.move(file_path, destination)
                organized += 1

        messagebox.showinfo("Success", f"Organized {organized} files into categories!")

if __name__ == "__main__":
    app = DownloadCleaner() 