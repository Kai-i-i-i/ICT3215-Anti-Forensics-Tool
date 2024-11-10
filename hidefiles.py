import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import subprocess
import platform
import random
from shutil import copyfile

# Default directory path for operations
default_directory = "C:\\HIDEFILE"

# Ensure the default directory exists
if not os.path.exists(default_directory):
    os.makedirs(default_directory)

# Function to hide the selected file by setting the hidden attribute or renaming it
def hide_file():
    file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Hide")
    if file_path:
        try:
            if platform.system() == "Windows":
                subprocess.check_call(["attrib", "+H", file_path])
                messagebox.showinfo("Success", f"The file has been hidden: {file_path}")
            else:
                directory, filename = os.path.split(file_path)
                hidden_file_path = os.path.join(directory, f".{filename}")
                os.rename(file_path, hidden_file_path)
                messagebox.showinfo("Success", f"The file has been hidden: {hidden_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("No file selected", "Please select a file to hide.")

# Function to list hidden files in the default directory
def list_hidden_files():
    hidden_files = []
    for filename in os.listdir(default_directory):
        file_path = os.path.join(default_directory, filename)
        if platform.system() == "Windows":
            if "H" in subprocess.check_output(["attrib", file_path]).decode():
                hidden_files.append(filename)
        else:
            if filename.startswith("."):
                hidden_files.append(filename)
    return hidden_files

# Function to unhide the selected hidden file
def unhide_file():
    hidden_files = list_hidden_files()
    if not hidden_files:
        messagebox.showinfo("No Hidden Files", "No hidden files found in the directory.")
        return

    select_window = tk.Toplevel(root)
    select_window.title("Select File to Unhide")
    select_window.geometry("400x200")
    select_window.configure(bg="#2e3b4e")

    label = ttk.Label(select_window, text="Select a hidden file to unhide:", background="#2e3b4e", foreground="white")
    label.pack(pady=10)

    file_var = tk.StringVar(value=hidden_files[0])
    dropdown = ttk.OptionMenu(select_window, file_var, *hidden_files)
    dropdown.pack(pady=10)

    def confirm_unhide():
        filename = file_var.get()
        file_path = os.path.join(default_directory, filename)
        try:
            if platform.system() == "Windows":
                subprocess.check_call(["attrib", "-H", file_path])
                messagebox.showinfo("Success", f"The file is now visible: {file_path}")
            else:
                if filename.startswith("."):
                    unhidden_file_path = os.path.join(default_directory, filename[1:])
                    os.rename(file_path, unhidden_file_path)
                    messagebox.showinfo("Success", f"The file is now visible: {unhidden_file_path}")
                else:
                    messagebox.showinfo("Already Visible", f"The file is already visible: {file_path}")
            select_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    unhide_button = ttk.Button(select_window, text="Unhide Selected File", command=confirm_unhide)
    unhide_button.pack(pady=10)

# Function to hide fake files in ADS of a primary file
def hide_fake_files_in_ads():
    primary_file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select Primary File for ADS")
    if primary_file_path:
        fake_files = {
            "bank_info.txt": """Account Holder: John Doe
Account Number: 987654321
Routing Number: 123456789
Bank: Offshore Savings Trust
Balance: $4,567,890.00
Notes: Monthly transfer to secure account.""",
            
            "confidential_report.pdf": """Project: Operation Eclipse
Classification: Top Secret
Objectives:
    - Phase I: Acquisition of assets in targeted regions
    - Phase II: Establish encrypted communications network
    - Phase III: Secure key personnel and operational funding
Timeline: Q3 2024 - Q1 2025
Warning: Unauthorized access is punishable by law.""",

            "passwords.docx": """Admin Portal: admin_portal.com
Username: johndoe_admin
Password: Sup3rS3cur3P@ssw0rd!

VPN Access: vpn.corpsecure.net
Username: jdoe_vpn
Password: Y3tAn0therS3curePass!

Email: john.doe@confidential.com
Password: email_4CC3$$!""",
        }

        for fake_filename, content in fake_files.items():
            ads_path = f"{primary_file_path}:{fake_filename}"
            with open(ads_path, "w") as ads_file:
                ads_file.write(content)
        messagebox.showinfo("Success", "Fake files have been hidden in ADS of the selected file.")

# Function to create a corrupt file by writing random data
def create_corrupt_file():
    file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Corrupt")
    if file_path:
        try:
            with open(file_path, "wb") as f:
                f.write(os.urandom(1024))  # Writes 1KB of random data
            messagebox.showinfo("Success", f"The file has been corrupted: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Function to lock a file by holding an exclusive open handle
def lock_file():
    global locked_file_handle

    file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Lock")
    if file_path:
        try:
            if platform.system() == "Windows":
                import win32file, win32con
                handle = win32file.CreateFile(
                    file_path,
                    win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                    0,
                    None,
                    win32con.OPEN_EXISTING,
                    0,
                    None
                )
                
                win32file.LockFileEx(
                    handle,
                    win32con.LOCKFILE_EXCLUSIVE_LOCK,
                    0,
                    0xffff0000,
                    win32file.OVERLAPPED()
                )
                messagebox.showinfo("Success", f"The file is now locked: {file_path}\nClose the application to release the lock.")
                
                locked_file_handle = handle
                
            else:
                import fcntl
                locked_file = open(file_path, "r+")
                fcntl.flock(locked_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                messagebox.showinfo("Success", f"The file is now locked: {file_path}\nClose the application to release the lock.")
                
                locked_file_handle = locked_file
                
        except BlockingIOError:
            messagebox.showerror("File Locked", "The file is already locked by another process.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("No file selected", "Please select a file to lock.")

# Function to create a copy of the file with a fake extension
def create_fake_extension_file():
    file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Copy with Fake Extension")
    if file_path:
        try:
            fake_extension = simpledialog.askstring("Fake Extension", "Enter the fake extension (e.g., .txt, .pdf, .jpg):")
            if fake_extension:
                if not fake_extension.startswith('.'):
                    fake_extension = f".{fake_extension}"
                
                base_name = os.path.splitext(file_path)[0]
                new_file_path = f"{base_name}{fake_extension}"
                
                copyfile(file_path, new_file_path)
                
                messagebox.showinfo("Success", f"A copy with the fake extension has been created: {new_file_path}")
            else:
                messagebox.showwarning("No Extension Entered", "Please enter a valid extension.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("No File Selected", "Please select a file to create with a fake extension.")

# Set up the Tkinter GUI
root = tk.Tk()
root.title("File Hider with Corrupt and Locked File Options")
root.geometry("500x600")
root.configure(bg="#2e3b4e")

title_label = ttk.Label(root, text="File Hider with Corrupt and Locked File Options", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)

hide_button = ttk.Button(root, text="Select File to Hide", command=hide_file, style="TButton")
hide_button.pack(pady=10)

unhide_button = ttk.Button(root, text="Select Hidden File to Unhide", command=unhide_file, style="TButton")
unhide_button.pack(pady=10)

ads_button = ttk.Button(root, text="Hide Fake Files in ADS", command=hide_fake_files_in_ads, style="TButton")
ads_button.pack(pady=10)

corrupt_button = ttk.Button(root, text="Create Corrupt File", command=create_corrupt_file, style="TButton")
corrupt_button.pack(pady=10)

lock_button = ttk.Button(root, text="Lock File", command=lock_file, style="TButton")
lock_button.pack(pady=10)

fake_extension_button = ttk.Button(root, text="Create File with Fake Extension", command=create_fake_extension_file, style="TButton")
fake_extension_button.pack(pady=10)

footer_label = ttk.Label(
    root,
    text="* Hidden files can be accessed with special commands as ADS streams.",
    font=("Helvetica", 8),
    foreground="light grey",
    background="#2e3b4e",
    wraplength=400
)
footer_label.pack(pady=10)

root.mainloop()
