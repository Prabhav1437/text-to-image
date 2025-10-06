import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox, scrolledtext
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import os
from datetime import datetime
import textwrap

class TextToImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text to Image Generator")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.text_color = (255, 255, 255)
        self.bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.font_size = tk.IntVar(value=24)
        self.image_width = tk.IntVar(value=800)
        self.image_height = tk.IntVar(value=600)
        self.current_image = None
        self.preview_image = None
        
        self.setup_ui()
        self.update_preview()
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Left panel - Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Text input
        ttk.Label(controls_frame, text="Enter Text:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.text_entry = scrolledtext.ScrolledText(controls_frame, width=30, height=8, wrap=tk.WORD)
        self.text_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.text_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # Font size
        ttk.Label(controls_frame, text="Font Size:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        font_frame = ttk.Frame(controls_frame)
        font_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Scale(font_frame, from_=12, to=72, variable=self.font_size, orient=tk.HORIZONTAL, 
                 command=lambda x: self.update_preview()).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(font_frame, textvariable=self.font_size).pack(side=tk.RIGHT)
        
        # Image dimensions
        ttk.Label(controls_frame, text="Image Size:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        size_frame = ttk.Frame(controls_frame)
        size_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(size_frame, text="Width:").grid(row=0, column=0, sticky=tk.W)
        width_scale = ttk.Scale(size_frame, from_=400, to=1920, variable=self.image_width, orient=tk.HORIZONTAL,
                               command=lambda x: self.update_preview())
        width_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Label(size_frame, textvariable=self.image_width).grid(row=0, column=2, padx=(5, 0))
        
        ttk.Label(size_frame, text="Height:").grid(row=1, column=0, sticky=tk.W)
        height_scale = ttk.Scale(size_frame, from_=300, to=1080, variable=self.image_height, orient=tk.HORIZONTAL,
                                command=lambda x: self.update_preview())
        height_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Label(size_frame, textvariable=self.image_height).grid(row=1, column=2, padx=(5, 0))
        
        size_frame.columnconfigure(1, weight=1)
        
        # Color controls
        color_frame = ttk.LabelFrame(controls_frame, text="Colors", padding="5")
        color_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(color_frame, text="Text Color", command=self.choose_text_color).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(color_frame, text="Background Color", command=self.choose_bg_color).grid(row=0, column=1, padx=(5, 0))
        ttk.Button(color_frame, text="Random Background", command=self.random_bg_color).grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Action buttons
        action_frame = ttk.Frame(controls_frame)
        action_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(action_frame, text="Generate & Preview", command=self.update_preview).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="Save Image", command=self.save_image).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="Open in Viewer", command=self.open_in_viewer).pack(fill=tk.X)
        
        # Right panel - Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Preview canvas with scrollbars
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        self.preview_canvas = tk.Canvas(canvas_frame, bg='white', width=400, height=300)
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.preview_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.preview_canvas.configure(xscrollcommand=h_scrollbar.set)
    
    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[0]:
            self.text_color = tuple(int(c) for c in color[0])
            self.update_preview()
    
    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[0]:
            self.bg_color = tuple(int(c) for c in color[0])
            self.update_preview()
    
    def random_bg_color(self):
        self.bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.update_preview()
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within the specified width"""
        lines = []
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append('')
                continue
                
            # Estimate characters per line based on average character width
            avg_char_width = font.getbbox('A')[2] - font.getbbox('A')[0]
            chars_per_line = max(1, int(max_width * 0.8 / avg_char_width))
            
            wrapped = textwrap.wrap(paragraph, width=chars_per_line)
            lines.extend(wrapped if wrapped else [''])
        
        return lines
    
    def generate_image(self):
        text = self.text_entry.get(1.0, tk.END).strip()
        if not text:
            return None
        
        width = self.image_width.get()
        height = self.image_height.get()
        
        # Create image
        image = Image.new('RGB', (width, height), self.bg_color)
        draw = ImageDraw.Draw(image)
        
        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", self.font_size.get())
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", self.font_size.get())
            except:
                font = ImageFont.load_default()
        
        # Wrap text
        margin = 40
        max_text_width = width - 2 * margin
        lines = self.wrap_text(text, font, max_text_width)
        
        # Calculate text positioning
        line_height = font.getbbox('Ay')[3] - font.getbbox('Ay')[1] + 5
        total_text_height = len(lines) * line_height
        start_y = (height - total_text_height) // 2
        
        # Draw text
        for i, line in enumerate(lines):
            if line.strip():  # Only draw non-empty lines
                line_bbox = font.getbbox(line)
                line_width = line_bbox[2] - line_bbox[0]
                x = (width - line_width) // 2
                y = start_y + i * line_height
                draw.text((x, y), line, fill=self.text_color, font=font)
        
        return image
    
    def update_preview(self):
        image = self.generate_image()
        if image:
            self.current_image = image
            
            # Create thumbnail for preview
            preview_size = (400, 300)
            preview_img = image.copy()
            preview_img.thumbnail(preview_size, Image.Resampling.LANCZOS)
            
            self.preview_image = ImageTk.PhotoImage(preview_img)
            
            # Update canvas
            self.preview_canvas.delete("all")
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # Center the image
            x = max(0, (canvas_width - preview_img.width) // 2)
            y = max(0, (canvas_height - preview_img.height) // 2)
            
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.preview_image)
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
    
    def save_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please generate an image first!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"text_image_{timestamp}.png"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialname=default_filename,
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_image.save(filename)
                messagebox.showinfo("Success", f"Image saved as {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def open_in_viewer(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please generate an image first!")
            return
        
        try:
            self.current_image.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")

def main():
    root = tk.Tk()
    app = TextToImageApp(root)
    root.state('zoomed')
    root.mainloop()

if __name__ == "__main__":
    main()