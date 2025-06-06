import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import sys
from pathlib import Path

class PQConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 HDR Image Converter 🔥")
        self.root.geometry("500x350")  # Made taller for the new button
        self.root.configure(bg='#1a1a1a')  # Dark background
        
        # Get the path to the ICC profile
        self.default_icc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ITUR_2100_PQ_FULL.ICC")
        self.current_icc = self.default_icc
        
        # Get ImageMagick path
        self.magick_path = self.get_magick_path()
        
        # Check HEIC support
        self.check_heic_support()
        
        # Create and pack widgets
        self.create_widgets()
        
    def get_magick_path(self):
        # Try to find ImageMagick in common locations
        possible_paths = [
            "/usr/local/bin/magick",  # Homebrew default
            "/opt/homebrew/bin/magick",  # Apple Silicon Homebrew
            "magick"  # Fallback to PATH
        ]
        
        for path in possible_paths:
            try:
                subprocess.run([path, "-version"], capture_output=True, check=True)
                return path
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
                
        return "magick"  # Fallback to PATH
        
    def check_heic_support(self):
        try:
            # Check if ImageMagick has HEIC support
            result = subprocess.run([self.magick_path, "-list", "format"], capture_output=True, text=True)
            self.heic_supported = "HEIC" in result.stdout
        except Exception:
            self.heic_supported = False
            
        if not self.heic_supported:
            messagebox.showwarning(
                "HEIC Support",
                "⚠️ HEIC support not detected. To convert HEIC files, please install ImageMagick with HEIC support:\n\n"
                "brew install imagemagick libheif"
            )
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="✨ HDR Image Converter ✨",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg='#1a1a1a'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Convert any image to HDR with PQ encoding 🌟",
            font=("Helvetica", 12),
            fg="#cccccc",
            bg='#1a1a1a'
        )
        subtitle_label.pack(pady=5)
        
        # ICC Profile Button
        self.icc_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.icc_frame.pack(pady=10)
        
        self.icc_button = tk.Button(
            self.icc_frame,
            text="🎨 Use Custom ICC Profile",
            command=self.select_icc_profile,
            font=("Helvetica", 12),
            bg='#2a2a2a',
            fg='#ffffff',
            relief="solid",
            borderwidth=2
        )
        self.icc_button.pack(side=tk.LEFT, padx=5)
        
        self.icc_label = tk.Label(
            self.icc_frame,
            text="(Using default PQ profile)",
            font=("Helvetica", 10),
            fg="#cccccc",
            bg='#1a1a1a'
        )
        self.icc_label.pack(side=tk.LEFT)
        
        # Drop zone
        self.drop_zone = tk.Label(
            self.root,
            text="🎨 Click here to select any image 🎨",
            font=("Helvetica", 14),
            width=40,
            height=8,
            relief="solid",
            borderwidth=2,
            bg='#2a2a2a',
            fg='#ffffff'
        )
        self.drop_zone.pack(pady=20, padx=20)
        
        # Bind click event
        self.drop_zone.bind("<Button-1>", self.handle_click)
        self.drop_zone.bind("<Enter>", lambda e: self.drop_zone.config(bg='#3a3a3a'))
        self.drop_zone.bind("<Leave>", lambda e: self.drop_zone.config(bg='#2a2a2a'))
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12),
            fg="#ffffff",
            bg='#1a1a1a'
        )
        self.status_label.pack(pady=10)
        
    def select_icc_profile(self):
        file_path = filedialog.askopenfilename(
            title="Select ICC Profile",
            filetypes=[("ICC Profiles", "*.icc *.icm"), ("All files", "*.*")]
        )
        if file_path:
            self.current_icc = file_path
            self.icc_label.config(text=f"(Using: {os.path.basename(file_path)})")
            self.icc_button.config(text="🔄 Change ICC Profile")
        
    def handle_click(self, event):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("All Images", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp *.gif *.heic *.heif"),
                ("iPhone Photos", "*.heic *.heif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("TIFF files", "*.tif *.tiff"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.process_file(file_path)
        
    def process_file(self, file_path):
        # Check if it's a HEIC file and if we support it
        if file_path.lower().endswith(('.heic', '.heif')) and not self.heic_supported:
            messagebox.showerror(
                "Error",
                "❌ HEIC support not available. Please install ImageMagick with HEIC support:\n\n"
                "brew install imagemagick libheif"
            )
            return
            
        # Generate output path
        output_path = os.path.splitext(file_path)[0] + "_hdr.png"
        
        # Convert the file
        self.convert(file_path, output_path)
        
    def convert(self, input_file, output_file):
        try:
            self.status_label.config(text="🔄 Converting...")
            self.root.update()
            
            # Run ImageMagick command
            cmd = [
                self.magick_path,
                input_file,
                "-define", "quantum:format=floating-point",
                "-depth", "16",
                "-profile", self.current_icc,
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.status_label.config(text="✅ Conversion completed successfully!")
                messagebox.showinfo("Success", f"✨ Image converted successfully!\nSaved as: {output_file}")
            else:
                self.status_label.config(text="❌ Conversion failed")
                messagebox.showerror("Error", f"❌ Conversion failed: {result.stderr}")
                
        except Exception as e:
            self.status_label.config(text="❌ Error occurred")
            messagebox.showerror("Error", f"❌ An error occurred: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PQConverterApp()
    app.run() 