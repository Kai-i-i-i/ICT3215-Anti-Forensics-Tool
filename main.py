import os
import platform
import subprocess
import time
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog, messagebox, ttk, simpledialog
from datetime import datetime, timedelta
import random
import win32evtlogutil
import win32evtlog
from cryptography.fernet import Fernet
import platform

# Generate a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)

def generate_random_ipv4():
    # Generate public IPv4 address
    while True:
        ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        if not (10 <= int(ip.split('.')[0]) <= 127 or ip.startswith("192.168") or ip.startswith("172.16")):
            return ip

def generate_random_ipv6():
    # Generate random IPv6 address
    return ":".join(f"{random.randint(0, 65535):x}" for _ in range(8))

class ForensicsDisruptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Forensics Disruptor")

        # Set up window dimensions
        self.root.geometry("600x700")

        # Title
        title = tk.Label(self.root, text="Forensics Disruptor", font=("Arial", 16))
        title.pack(pady=10)

        # Log Forgery Section
        log_forgery_label = tk.Label(self.root, text="Log Forgery", font=("Arial", 14))
        log_forgery_label.pack(pady=10)

        # Timestamp Manipulation Button
        timestamp_button = tk.Button(self.root, text="Alter Timestamps", command=self.alter_timestamps)
        timestamp_button.pack(pady=5)

        # Inject Fake User Activity Button
        fake_activity_button = tk.Button(self.root, text="Inject Fake User Activity", command=self.inject_fake_activity)
        fake_activity_button.pack(pady=5)

        # Mask Unauthorized Actions Button
        mask_actions_button = tk.Button(self.root, text="Mask Unauthorized Actions", command=self.mask_unauthorized_actions)
        mask_actions_button.pack(pady=5)

        # Phantom Files Section
        phantom_files_label = tk.Label(self.root, text="Phantom Files", font=("Arial", 14))
        phantom_files_label.pack(pady=10)

        # Create Phantom File Button
        phantom_file_button = tk.Button(self.root, text="Create Phantom File", command=self.create_phantom_file)
        phantom_file_button.pack(pady=5)

        # Sparse Files Button
        sparse_file_button = tk.Button(self.root, text="Create Sparse Files", command=self.create_sparse_files)
        sparse_file_button.pack(pady=5)

        # Conceal Files Section
        conceal_files_label = tk.Label(self.root, text="Conceal Files", font=("Arial", 14))
        conceal_files_label.pack(pady=10)

        # Conceal Files with Symbolic Links
        conceal_files_button = tk.Button(self.root, text="Conceal Files (Sym Links)", command=self.conceal_files)
        conceal_files_button.pack(pady=5)

        # Conceal Files in NTFS ADS
        conceal_files_button = tk.Button(self.root, text="Conceal Files (NTFS ADS)", command=self.conceal_files_ads)
        conceal_files_button.pack(pady=5)

        # Corrupt/Locked Files Button
        corrupt_files_button = tk.Button(self.root, text="Create Corrupt/Locked Files", command=self.create_corrupt_files)
        corrupt_files_button.pack(pady=5)

        # Fake File Extension Button
        fake_extension_button = tk.Button(self.root, text="Create Files with Fake Extensions", command=self.create_fake_extension)
        fake_extension_button.pack(pady=5)

        # Metadata Manipulation Section
        metadata_label = tk.Label(self.root, text="File Metadata Manipulation", font=("Arial", 14))
        metadata_label.pack(pady=10)

        # Metadata Manipulation Button
        metadata_button = tk.Button(self.root, text="Manipulate File Metadata", command=self.manipulate_metadata)
        metadata_button.pack(pady=5)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack(pady=10)

    # Log Forgery Functions
    def alter_timestamps(self):
        source_name = "FakeSource"
        message = simpledialog.askstring("Altered Log", "Enter the message to include in the forged log: ")

        # Set a custom timestamp (7 days ago)
        custom_time = datetime.now() - timedelta(days=7)
        custom_time_str = custom_time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Register the event source if it doesn't already exist
            win32evtlogutil.AddSourceToRegistry(source_name, "Application")
        except Exception as e:
            print(f"Source already exists: {e}")

        try:
            # Report the event with the custom timestamp (as part of the string)
            # Note: Event logs do not allow direct setting of the timestamp, so it's included in the message
            win32evtlogutil.ReportEvent(
                source_name,
                eventID=1003,  # New event ID for backdated log
                eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
                strings=[f"[Timestamp: {custom_time_str}] {message}"]
            )
            print(f"[+] Forged log with custom timestamp written: {custom_time_str}")
        except Exception as e:
            print(f"Failed to write log: {e}")

    def inject_fake_activity(self):
        source_name = "Application"  # Write to Application log

        # Prompt for user input through dialog boxes
        user = simpledialog.askstring("Inject Fake Activity", "Enter the username to inject activity for:")
        if not user:
            messagebox.showwarning("Input Required", "Username is required.")
            return

        activity = simpledialog.askstring("Inject Fake Activity", "Enter the activity (e.g., login, logout):")
        if not activity:
            messagebox.showwarning("Input Required", "Activity is required.")
            return

        # Generate a random IP address
        ip_address = generate_random_ipv4() if random.random() < 0.8 else generate_random_ipv6()

        # Define the message based on activity type
        if activity.lower() == "login":
            event_id = 4624  # Event ID for successful login
            message = (
                f"An account was successfully logged on.\n"
                f"Subject:\n"
                f"\tSecurity ID: SYSTEM\n"
                f"\tAccount Name: {user}\n"
                f"\tLogon ID: 0x3E7\n"
                f"Network Information:\n"
                f"\tSource Network Address: {ip_address}\n"
            )
        elif activity.lower() == "logout":
            event_id = 4634  # Event ID for logoff
            message = (
                f"An account was logged off.\n"
                f"Subject:\n"
                f"\tSecurity ID: SYSTEM\n"
                f"\tAccount Name: {user}\n"
                f"\tLogon ID: 0x3E7\n"
            )
        else:
            messagebox.showerror("Invalid Input", "Activity must be 'login' or 'logout'.")
            return

        # Write the event to Event Viewer
        try:
            win32evtlogutil.ReportEvent(
                source_name,
                eventID=event_id,
                eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
                strings=[message]
            )
            messagebox.showinfo("Success", f"Fake user activity injected for user '{user}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to inject activity: {e}")

    def mask_unauthorized_actions(self):
        source_name = "Application"

        # Prompt for user input through dialog boxes
        user = simpledialog.askstring("mask unauthorized actions", "Enter the username to mask:")
        if not user:
            messagebox.showwarning("Input Required", "Username is required.")
            return

        unauthorized_event_id = 4625  # Failed login
        authorized_event_id = 4624  # Successful login

        ip_address = generate_random_ipv4() if random.random() < 0.8 else generate_random_ipv6()

        message = (
            f"An account was successfully logged on.\n"
            f"Subject:\n"
            f"\tSecurity ID: SYSTEM\n"
            f"\tAccount Name: {user}\n"
            f"\tLogon ID: 0x3E7\n"
            f"Network Information:\n"
            f"\tSource Network Address: {ip_address}\n"
        )

        try:
            print(f"[DEBUG] Writing masked action to {source_name} log...")
            win32evtlogutil.ReportEvent(
                source_name,
                eventID=authorized_event_id,
                eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
                strings=[message]
            )
            print(f"[+] Unauthorized action masked for user '{user}' in {source_name} log.")
        except Exception as e:
            print(f"[!] Failed to mask unauthorized action: {e}")

    # Phantom Files Functions
    def create_phantom_file(self):
        # Let user select the folder to create the phantom file
        filepath = filedialog.askdirectory(title="Select Folder to Create Phantom File")
        if filepath:
            # Prompt the user to choose a file extension
            file_extension = simpledialog.askstring("File Extension", "Enter file extension (e.g., .txt, .log, .dat):")

            if file_extension:
                # Ensure the extension starts with a dot
                if not file_extension.startswith('.'):
                    file_extension = f".{file_extension}"

                # Start with the base file name
                base_filename = "phantom_file1"
                phantom_file_path = os.path.join(filepath, f"{base_filename}{file_extension}")

                # Check if the file already exists, if so, append a number to the name
                counter = 1
                while os.path.exists(phantom_file_path):
                    phantom_file_path = os.path.join(filepath, f"{base_filename}_{counter}{file_extension}")
                    counter += 1

                # Create the phantom file (empty file for example)
                with open(phantom_file_path, 'w') as phantom_file:
                    phantom_file.write("This is a phantom file.")

                # Hide the file (Windows-specific hiding via attrib, for other OS hidden by default)
                if platform.system() == "Windows":
                    try:
                        # Make the file hidden in Windows
                        subprocess.check_call(["attrib", "+H", phantom_file_path])
                        messagebox.showinfo("Success", f"Hidden phantom file created: {phantom_file_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to hide the file: {e}")
                else:
                    # On Linux/Mac, the file is hidden by default due to the dot prefix
                    messagebox.showinfo("Success", f"Hidden phantom file created: {phantom_file_path}")
            else:
                messagebox.showwarning("No Extension", "Please enter a valid file extension.")

    def create_sparse_files(self):
        # Let user choose the directory to save the sparse file
        filepath = filedialog.askdirectory(title="Select Folder to Create Sparse File")

        if filepath:
            file_name = "sparse_file.txt"  # Name of the sparse file
            sparse_file_path = os.path.join(filepath, file_name)

            try:
                # Open the file with O_CREAT and O_RDWR flags
                fd = os.open(sparse_file_path, os.O_CREAT | os.O_RDWR)

                # Set the file size (allocate space without writing data to it)
                file_size = 10 * 1024 * 1024  # 10 MB for example
                os.lseek(fd, file_size - 1, os.SEEK_SET)  # Move the file pointer to the last byte
                os.write(fd, b'\0')  # Write a single byte to mark the space as allocated

                os.close(fd)
                messagebox.showinfo("Success", f"Sparse file created at: {sparse_file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    # Conceal Files Functions
    def conceal_files(self):
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

    # Function to hide fake files in ADS of a primary file
    def conceal_files_ads(self):
        primary_file_path = filedialog.askopenfilename(initialdir=default_directory,
                                                       title="Select Primary File for ADS")
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

    def create_corrupt_files(self):
        # Ask the user whether they want to corrupt or lock the file
        action = simpledialog.askstring("Select Action", "Choose action: 'corrupt' or 'lock'")

        if action not in ["corrupt", "lock"]:
            messagebox.showwarning("Invalid Input", "Please enter either 'corrupt' or 'lock'.")
            return
        file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Corrupt")
        if file_path:
            try:
                if action == "corrupt":
                    # Corrupt the file by writing random data
                    with open(file_path, "wb") as f:
                        f.write(os.urandom(1024))  # Writes 1KB of random data
                    messagebox.showinfo("Success", f"The file has been corrupted: {file_path}")

                elif action == "lock":
                    global locked_file_handle
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
                            messagebox.showinfo("Success",
                                                f"The file is now locked: {file_path}\nClose the application to release the lock.")

                            locked_file_handle = handle

                        else:
                            import fcntl
                            locked_file = open(file_path, "r+")
                            fcntl.flock(locked_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                            messagebox.showinfo("Success",
                                                f"The file is now locked: {file_path}\nClose the application to release the lock.")

                            locked_file_handle = locked_file

                    except BlockingIOError:
                        messagebox.showerror("File Locked", "The file is already locked by another process.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("No file selected", "Please select a file to corrupt or lock.")

    def create_fake_extension(self):
        file_path = filedialog.askopenfilename(initialdir=default_directory,
                                               title="Select File to Rename with Fake Extension")
        if file_path:
            try:
                fake_extension = simpledialog.askstring("Fake Extension",
                                                        "Enter the fake extension (e.g., .txt, .pdf, .jpg):")
                if fake_extension:
                    if not fake_extension.startswith('.'):
                        fake_extension = f".{fake_extension}"

                    base_name = os.path.splitext(file_path)[0]
                    new_file_path = f"{base_name}{fake_extension}"

                    os.rename(file_path, new_file_path)

                    messagebox.showinfo("Success", f"The file has been renamed to: {new_file_path}")
                else:
                    messagebox.showwarning("No Extension Entered", "Please enter a valid extension.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("No File Selected", "Please select a file to rename with a fake extension.")

    # File Metadata Manipulation Functions
    def manipulate_metadata(self):
        """
        Select a file and apply metadata manipulation, timestamp modification,
        and encryption as part of anti-forensics techniques.
        """
        filepath = filedialog.askopenfilename()
        if not filepath:
            messagebox.showwarning("No File Selected", "Please select a file.")
            return

        # Step 1: Create an encrypted version of the file
        encrypted_filepath = self.create_encrypted_similar_file(
            filepath, content="Classified details about Project X."
        )
        if encrypted_filepath:
            messagebox.showinfo(
                "Success", f"Encrypted file created: {encrypted_filepath}"
            )
        # Step 2: Hide the original file
        self.hide_file(encrypted_filepath)
        # Step 3: Modify timestamps
        self.modify_file_timestamp(encrypted_filepath)
        messagebox.showinfo(
            "Success", f"Timestamps updated for: {encrypted_filepath}"
        )

        # Step 4: Manipulate metadata (Linux only)
        if platform.system() == 'Linux' or os.name == 'posix':
            self.manipulate_file_metadata(encrypted_filepath, new_owner="nobody", new_group="nogroup")
            messagebox.showinfo(
                "Success",
                f"Metadata manipulated for: {encrypted_filepath} (Linux only).",
            )
        else:
            messagebox.showwarning("Notice", "Metadata manipulation is not applicable on this platform. Skipping this step...")

    # Helper functions for manipulate_metadata() start
    def modify_file_timestamp(self, file_path):
        """Modify the timestamp of a file to a random time within the last 5 years."""
        try:
            start_date = datetime.now() - timedelta(days=5 * 365)
            end_date = datetime.now()
            random_date = start_date + (end_date - start_date) * random.random()
            timestamp = time.mktime(random_date.timetuple())
            os.utime(file_path, (timestamp, timestamp))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to modify timestamps: {e}")

    def manipulate_file_metadata(self, file_path, new_owner="fake_user", new_group="fake_group"):
        """
        Manipulate file metadata (requires root/administrator privileges on some systems).
        """
        if platform.system() == 'Linux' or os.name == 'posix':
            os.system(f"chown {new_owner}:{new_group} {file_path}")
        else:
            messagebox.showwarning("Warning", "Skipping step for metadata manipulation for Linux...")

    def create_encrypted_similar_file(self,original_file_path, content="Sensitive information."):
        """
        Create a similar encrypted file with '_confidential' added to the original filename.
        Skip if the file already ends with '_confidential'.
        """
        dir_name, original_file_name = os.path.split(original_file_path)

        # Check if the file already ends with '_confidential'
        if original_file_name.endswith("_confidential" + os.path.splitext(original_file_name)[1]):
            print(f"File {original_file_name} already ends with '_confidential'. Skipping creation.")
            return original_file_path  # Return the original file path to apply anti-forensics

        # Create a new file name by appending "_confidential" to the original file name
        confidential_file_name = os.path.splitext(original_file_name)[0] + "_confidential" + \
                                 os.path.splitext(original_file_name)[1]
        confidential_file_path = os.path.join(dir_name, confidential_file_name)

        try:
            # Encrypt the content and write it to the new confidential file
            encrypted_content = cipher.encrypt(content.encode())
            with open(confidential_file_path, 'wb') as confidential_file:
                confidential_file.write(encrypted_content)
            print(f"Encrypted similar file created at {confidential_file_path}. Content is misleading and encrypted.")
            return confidential_file_path
        except PermissionError:
            print(f"Permission denied: Unable to create or write to the file at {confidential_file_path}.")
            return None
        except Exception as e:
            print(f"An error occurred while creating the file: {e}")
            return None

    def hide_file(self, file_path):
        """
        Hide a file by setting its 'hidden' attribute.
        """
        try:
            if platform.system() == 'Windows':
                os.system(f'attrib +h "{file_path}"')
                print(f"{file_path} is now hidden.")
            else:
                dir_name, file_name = os.path.split(file_path)
                hidden_file_path = os.path.join(dir_name, '.' + file_name)
                os.rename(file_path, hidden_file_path)
                print(f"{file_path} renamed to {hidden_file_path} to hide it.")
        except FileNotFoundError:
            print(f"File {file_path} not found. Cannot hide the file.")
        except Exception as e:
            print(f"An error occurred while hiding the file: {e}")
    # Helper functions for manipulate_metadata() end
    
# Run the application
if __name__ == "__main__":
    # Default directory path for operations
    default_directory = "test_folder"

    # Ensure the default directory exists
    if not os.path.exists(default_directory):
        os.makedirs(default_directory)
    root = tk.Tk()
    app = ForensicsDisruptorApp(root)
    root.mainloop()
