import os
import platform
import subprocess
import time
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog, messagebox, ttk, simpledialog
from datetime import datetime, timedelta
import random


def generate_random_timestamp():
    """
    Generate a random timestamp within the last 5 years.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)  # Approximately 5 years ago
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

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

        # Log File Poisoning (Optional)
        log_poisoning_button = tk.Button(self.root, text="Log File Poisoning", command=self.log_file_poisoning)
        log_poisoning_button.pack(pady=5)

        # Phantom Files Section
        phantom_files_label = tk.Label(self.root, text="Phantom Files", font=("Arial", 14))
        phantom_files_label.pack(pady=10)

        # Create Phantom File Button
        phantom_file_button = tk.Button(self.root, text="Create Phantom File", command=self.create_phantom_file)
        phantom_file_button.pack(pady=5)

        # In-Memory Files (Optional)
        in_memory_button = tk.Button(self.root, text="Create In-Memory Files", command=self.create_in_memory_file)
        in_memory_button.pack(pady=5)

        # Sparse Files Button
        sparse_file_button = tk.Button(self.root, text="Create Sparse Files", command=self.create_sparse_files)
        sparse_file_button.pack(pady=5)

        # Conceal Files Section
        conceal_files_label = tk.Label(self.root, text="Conceal Files", font=("Arial", 14))
        conceal_files_label.pack(pady=10)

        # Conceal Files with Symbolic Links/NTFS ADS
        conceal_files_button = tk.Button(self.root, text="Conceal Files (Sym Links/NTFS ADS)", command=self.conceal_files)
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
        """Alter the timestamps of a selected file."""
        # Prompt user to select a file
        file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Alter Timestamp")
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a file to alter its timestamps.")
            return

        # Generate a random timestamp
        new_time = generate_random_timestamp()

        try:
            # Convert the random timestamp to a UNIX timestamp
            time_struct = time.strptime(new_time, '%Y-%m-%d %H:%M:%S')
            timestamp = time.mktime(time_struct)

            # Update the file's access and modification times
            os.utime(file_path, (timestamp, timestamp))

            # Notify the user of the successful operation
            messagebox.showinfo("Success", f"Timestamps for {file_path} modified to {new_time}.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {file_path} not found. Cannot modify timestamp.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while modifying the timestamp: {e}")

    def inject_fake_activity(self):
        # Placeholder for injecting fake user activity logic
        messagebox.showinfo("Info", "Injecting Fake User Activity...")

    def mask_unauthorized_actions(self):
        # Placeholder for masking unauthorized actions logic
        messagebox.showinfo("Info", "Masking Unauthorized Actions...")

    def log_file_poisoning(self):
        # Placeholder for log file poisoning (optional)
        messagebox.showinfo("Info", "Running Log File Poisoning...")

    # Phantom Files Functions
    def create_phantom_file(self):
        # Let user select the folder to create the phantom file
        filepath = filedialog.askdirectory(title="Select Folder to Create Phantom File")
        if filepath:
            # Create a phantom file (empty file for example)
            phantom_file_path = os.path.join(filepath, "phantom_file.txt")
            with open(phantom_file_path, 'w') as phantom_file:
                phantom_file.write("This is a phantom file.")

    def create_in_memory_file(self):
        # Placeholder for creating in-memory files logic (optional)
        messagebox.showinfo("Info", "Creating In-Memory Files...")

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
        filepath = filedialog.askdirectory()
        messagebox.showinfo("Info", f"Concealing Files in {filepath}...")
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
    def hide_fake_files_in_ads(self):
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
        file_path = filedialog.askopenfilename(initialdir=default_directory, title="Select File to Corrupt")
        if file_path:
            try:
                with open(file_path, "wb") as f:
                    f.write(os.urandom(1024))  # Writes 1KB of random data
                messagebox.showinfo("Success", f"The file has been corrupted: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def lock_file(self):
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
            messagebox.showwarning("No file selected", "Please select a file to lock.")

    def create_fake_extension(self):
        file_path = filedialog.askopenfilename(initialdir=default_directory,
                                               title="Select File to Copy with Fake Extension")
        if file_path:
            try:
                fake_extension = simpledialog.askstring("Fake Extension",
                                                        "Enter the fake extension (e.g., .txt, .pdf, .jpg):")
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

        # Step 2: Modify timestamps
        self.modify_file_timestamp(encrypted_filepath)
        messagebox.showinfo(
            "Success", f"Timestamps updated for: {encrypted_filepath}"
        )

        # Step 3: Manipulate metadata (Linux only)
        self.manipulate_file_metadata(encrypted_filepath, new_owner="nobody", new_group="nogroup")
        messagebox.showinfo(
            "Success",
            f"Metadata manipulated for: {encrypted_filepath} (Linux only).",
        )

    def create_encrypted_similar_file(self, original_file_path, content):
        """
        Create a new file with "_confidential" in the name containing specified content.
        """
        directory, filename = os.path.split(original_file_path)
        new_filename = (
            filename.replace(".txt", "_confidential.txt")
            if filename.endswith(".txt")
            else f"{filename}_confidential"
        )
        new_file_path = os.path.join(directory, new_filename)

        try:
            with open(new_file_path, "w") as file:
                file.write(content)
            return new_file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create encrypted file: {e}")
            return None

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
        if platform.system() == 'Linux':
            os.system(f"chown {new_owner}:{new_group} {file_path}")
        else:
            print("Metadata manipulation is limited on this OS.")

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
