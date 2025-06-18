import tkinter as tk
from tkinter import filedialog, messagebox
import os
from itertools import groupby
import shutil
from datetime import datetime

#Main window
root = tk.Tk()
root.title("Transcription Highlight Widget")
root.geometry("400x400")

labelo = tk.Label(root, text="Hello! Select a folder. All duplicates MMDDYYYY-1#\n will move to a folder labelled separated_[timestamp]\n in the same folder which you chose.", font=("Arial", 12))
labelo.pack(pady=20)
labela = tk.Label(root, text="Folder_In", font=("Arial", 12))
labela.pack(pady=20)
label1 = tk.Label(root, text="NONE SELECTED", font=("Arial", 12))
label1.pack(pady=20)

output_folder_path = None

def open_folder_picker(label):
    global output_folder_path
    try:
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            label.config(text=f"Folder: {folder_path}")
            output_folder_path = folder_path
        else:
            label.config(text="NONE SELECTED")
            output_folder_path = None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while selecting the folder: {e}")
        label.config(text="NONE SELECTED")
        output_folder_path = None


def remove_dups(folder_path):
    if folder_path is None:
        messagebox.showerror("Error", "Please select a folder before removing duplicates.")
        return
    try:
        files = os.listdir(folder_path)
        print(files)
        base_files = {}
        to_move = []
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        separated_folder = os.path.join(folder_path, f"separated_{timestamp}")
        os.makedirs(separated_folder, exist_ok=True)

        for file in files:
            check = str(file)[:9] + str(file)[10:]
            print("Check:", check)
            if check in files:
                to_move.append(file)
                print("Duplicate found:", file)
        
        if not to_move:
            messagebox.showinfo("Result", "No duplicates found to move.")
        else:
            for file_name in to_move:
                src_path = os.path.join(folder_path, file_name)
                dst_path = os.path.join(separated_folder, file_name)
                shutil.move(src_path, dst_path)
            messagebox.showinfo("Result", f"Moved {len(to_move)} duplicates to 'separated/' folder.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        

#Decision Buttons
button1 = tk.Button(root, text="Select File Folder", command=lambda: open_folder_picker(label1))
button1.pack(pady=10)
button3 = tk.Button(root, text="Remove MMDDYY-1# Files.", command=lambda: remove_dups(output_folder_path))
button3.pack(pady=10)

#Run
root.mainloop()