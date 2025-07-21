import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime

BG_COLOR = "#f0f4f8"
FG_COLOR = "#1f2937"
BUTTON_COLOR = "#3b82f6"
BUTTON_HOVER = "#2563eb"
FRAME_COLOR = "#e5e7eb"
FONT_HEADER = ("Helvetica", 16, "bold")
FONT_NORMAL = ("Helvetica", 11)
FONT_SMALL = ("Helvetica", 10)

root = tk.Tk()
root.title("Transcription Highlight Widget")
root.geometry("500x420")
root.configure(bg=BG_COLOR)

main_frame = tk.Frame(root, bg=FRAME_COLOR, bd=2, relief="ridge", padx=20, pady=20)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

header = tk.Label(main_frame, text="🗂️ Transcription Duplicate Mover", bg=FRAME_COLOR, fg=FG_COLOR, font=FONT_HEADER)
header.pack(pady=(0, 15))

instructions = tk.Label(
    main_frame,
    text="Select a folder. All duplicates named MMDDYYYY-1# will be moved\n"
         "to a new folder labeled 'separated_<timestamp>'\n"
         "in the same selected directory.",
    bg=FRAME_COLOR,
    fg=FG_COLOR,
    font=FONT_SMALL,
    justify="center"
)
instructions.pack(pady=(0, 15))

labela = tk.Label(main_frame, text="📁 Selected Folder:", bg=FRAME_COLOR, fg=FG_COLOR, font=FONT_NORMAL)
labela.pack()

label1 = tk.Label(main_frame, text="NONE SELECTED", bg="white", fg=FG_COLOR, font=FONT_SMALL, relief="sunken", width=50, anchor="w")
label1.pack(pady=(0, 15))

output_folder_path = None

def open_folder_picker(label):
    global output_folder_path
    try:
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            label.config(text=folder_path)
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
        to_move = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        separated_folder = os.path.join(folder_path, f"separated_{timestamp}")
        os.makedirs(separated_folder, exist_ok=True)

        for file in files:
            check = str(file)[:9] + str(file)[10:]
            if check in files:
                to_move.append(file)

        if not to_move:
            messagebox.showinfo("Result", "No duplicates found to move.")
        else:
            for file_name in to_move:
                src_path = os.path.join(folder_path, file_name)
                dst_path = os.path.join(separated_folder, file_name)
                shutil.move(src_path, dst_path)
            messagebox.showinfo("Result", f"Moved {len(to_move)} duplicates to the 'separated' folder.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_enter(e): e.widget.config(bg=BUTTON_HOVER)
def on_leave(e): e.widget.config(bg=BUTTON_COLOR)

button1 = tk.Button(main_frame, text="📂 Select Folder", bg=BUTTON_COLOR, fg="white", font=FONT_NORMAL, relief="flat", padx=10, pady=5,
                    command=lambda: open_folder_picker(label1))
button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)
button1.pack(pady=8)

button2 = tk.Button(main_frame, text="🚮 Remove MMDDYYYY-1# Files", bg=BUTTON_COLOR, fg="white", font=FONT_NORMAL, relief="flat", padx=10, pady=5,
                    command=lambda: remove_dups(output_folder_path))
button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)
button2.pack(pady=8)

footer = tk.Label(main_frame, text="✨ Made with Tkinter", bg=FRAME_COLOR, fg="#6b7280", font=FONT_SMALL)
footer.pack(side="bottom", pady=10)

root.mainloop()
