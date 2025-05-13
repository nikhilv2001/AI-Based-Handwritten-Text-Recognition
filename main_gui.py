import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
from PIL import Image, ImageTk
import pytesseract
import os

#Configure the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Nikhil Verma\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Function to save as text file
def save_text_to_file():
    # Get all text from the Listbox
    lines = event_list.get(0, tk.END)
    if not lines:
        messagebox.showwarning("Warning", "No extracted text to save!")
        return
    try:
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        messagebox.showinfo("Success", "Extracted text saved as 'extracted_text.txt' successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save text: {e}")
        
# Function to browse file
def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        plate_no_entry.delete(0, tk.END)
        plate_no_entry.insert(0, filepath)
        show_image(filepath)

# Function to show selected image
def show_image(filepath):
    img = Image.open(filepath)
    img = img.resize((300, 300))  # Resize for preview
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# Function to extract text
def handle_Text_Extraction():
    filepath = plate_no_entry.get()
    if not filepath:
        messagebox.showwarning("Warning", "Please select an image file first!")
        return
    try:
        extracted_text = pytesseract.image_to_string(Image.open(filepath))
        lines = extracted_text.strip().split('\n')
        update_event_list(lines)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract text: {e}")

# Function to update extracted text in list
def update_event_list(lines):
    event_list.delete(0, tk.END)
    for line in lines:
        if line.strip():
            event_list.insert(tk.END, line)

# Create Main GUI window
root = tk.Tk()
root.title("Handwritten Text Extraction Tool")
root.geometry("1000x700")
root.configure(padx=10, pady=10)

# ============ First Row - File Browser ============
first_row = tk.Frame(root)
first_row.pack(fill=tk.X, pady=5)

plate_no_entry = tk.Entry(first_row, width=80)
plate_no_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

browse_button = tk.Button(first_row, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=5)

# ============ Second Row - Image Preview and Options ============
second_row = tk.Frame(root)
second_row.pack(fill=tk.BOTH, expand=True, pady=5)

# Left Column - Image Preview
left_col = tk.Frame(second_row)
left_col.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

image_label = tk.Label(left_col,  width=300, height=300)
image_label.pack(fill=tk.BOTH, expand=True)

# Right Column - Options
right_col = tk.Frame(second_row)
right_col.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

options_label = tk.Label(right_col, text="Image Processing Options", font=("Arial", 14))
options_label.pack(pady=10)

# Add your options here (example: Binarization)
'''
binarize_var = tk.IntVar()
binarize_checkbox = tk.Checkbutton(right_col, text="Apply Binarization", variable=binarize_var)
binarize_checkbox.pack(anchor='w', padx=10)
'''
extract_button = tk.Button(right_col, text="Extract Text", command=handle_Text_Extraction)
extract_button.pack(pady=20)

# ============ Third Row - Extracted Text List ============
third_row = tk.Frame(root)
third_row.pack(fill=tk.BOTH, expand=True, pady=5)
 

# Create a subframe to hold label and button side by side
label_button_frame = tk.Frame(third_row)
label_button_frame.pack(fill=tk.X)

event_list_label = tk.Label(label_button_frame, text="Extracted Text Result:", font=("Arial", 14))
event_list_label.pack(side=tk.LEFT)

save_button = tk.Button(label_button_frame, text="Save As Text", command=save_text_to_file)
save_button.pack(side=tk.RIGHT, padx=10)
 

listbox_frame = tk.Frame(third_row)
listbox_frame.pack(fill=tk.BOTH, expand=True)

event_list = tk.Listbox(listbox_frame)
event_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(listbox_frame, orient=tk.VERTICAL, command=event_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

event_list.config(yscrollcommand=scrollbar.set)

root.mainloop()
