import os
import platform
import subprocess
import time
import string
import tkinter as tk
from shutil import copyfile
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime, timedelta
import random
import win32evtlogutil
import win32evtlog
from cryptography.fernet import Fernet
import platform

# Generate a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)

# Helper functions
def generate_random_ipv4():
    # Generate public IPv4 address
    while True:
        ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        if not (10 <= int(ip.split('.')[0]) <= 127 or ip.startswith("192.168") or ip.startswith("172.16")):
            return ip

def generate_random_ipv6():
    # Generate random IPv6 address
    return ":".join(f"{random.randint(0, 65535):x}" for _ in range(8))

def create_random_extension(length=3):
    """Generate a random extension of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

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

        # Inject Fake User Activity Section
        activity_label = tk.Label(self.root, text="Select User Activity to Inject:", font=("Arial", 12))
        activity_label.pack(pady=5)  # Add a label for clarity

        # Inject Fake User Activity Dropdown
        global activity_var
        activity_var = tk.StringVar(self.root)  # Create a StringVar for the dropdown
        activity_var.set(activities[0])  # Set the default value

        activity_menu = tk.OptionMenu(self.root, activity_var, *activities)  # Create the dropdown menu
        activity_menu.pack(pady=5)  # Pack the dropdown menu into the window

        # Inject Fake User Activity Button
        inject_activity_button = tk.Button(self.root, text="Inject Selected Activity", command=self.inject_fake_activity)
        inject_activity_button.pack(pady=5)

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
        sources = ["Application", "Security", "System", "Setup", "Forwarded Events"]  # List of valid Windows log sources
        event_ids = [4624, 4625, 4634, 1000, 1001, 1002]  # List of valid event IDs
        messages = [
            "User logged in successfully.",
            "User failed to log in.",
            "User logged off.",
            "Application started.",
            "Application stopped.",
            "System rebooted."
        ]

        used_sources = set()  # Track used sources
        used_messages = set()  # Track used messages

        for _ in range(5):  # Inject and alter 5 times
            time.sleep(1)  # Sleep for 1 second before each loop cycle
            
            # Select a unique source
            source_name = random.choice([s for s in sources if s not in used_sources])
            used_sources.add(source_name)

            # Select a unique event ID
            event_id = random.choice(event_ids)  # Randomly select an event ID

            # Select a unique message
            message = random.choice([m for m in messages if m not in used_messages])
            used_messages.add(message)

            # Set a custom timestamp (7 days ago)
            custom_time = datetime.now() - timedelta(days=7)
            custom_time_str = custom_time.strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Register the event source if it doesn't already exist
                win32evtlogutil.AddSourceToRegistry(source_name, "Application")
            except Exception as e:
                messagebox.showerror("Error", f"Source already exists: {e}")

            try:
                # Report the event with the custom timestamp (as part of the string)
                win32evtlogutil.ReportEvent(
                    source_name,
                    eventID=event_id,  # Use the randomly selected event ID
                    eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
                    strings=[f"[Timestamp: {custom_time_str}] {message}"]
                )
                messagebox.showinfo("Success", f"[+] Forged log with custom timestamp written: {custom_time_str} from source: {source_name} with event ID: {event_id}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to write log: {e}")

    def inject_fake_activity(self):
        source_name = "Application"  # Write to Application log

        # Prompt for user input through dialog boxes
        user = simpledialog.askstring("Inject Fake Activity", "Enter the username to inject activity for:")
        if not user:
            messagebox.showwarning("Input Required", "Username is required.")
            return

        # Generate a random IP address
        ip_address = generate_random_ipv4() if random.random() < 0.8 else generate_random_ipv6()

        # Get the selected activity from the dropdown
        activity = activity_var.get()  # Use the dropdown variable instead of asking for input

        # Check if an activity was selected
        if not activity:
            messagebox.showwarning("Input Required", "Activity type is required.")
            return

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
        elif activity.lower() == "file_access":
            event_id = 4663  # Event ID for file access
            message = (
                f"File accessed by user.\n"
                f"Subject:\n"
                f"\tSecurity ID: SYSTEM\n"
                f"\tAccount Name: {user}\n"
                f"\tLogon ID: 0x3E7\n"
                f"Network Information:\n"
                f"\tSource Network Address: {ip_address}\n"
            )
        elif activity.lower() == "system_shutdown":
            event_id = 6006  # Event ID for system shutdown
            message = (
                f"System shutdown initiated by user.\n"
                f"Subject:\n"
                f"\tSecurity ID: SYSTEM\n"
                f"\tAccount Name: {user}\n"
                f"\tLogon ID: 0x3E7\n"
            )
        else:
            messagebox.showwarning("Invalid Activity", "Please enter a valid activity type.")
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
        folder_path = filedialog.askdirectory(title="Select Folder to Rename Files with Fake Extensions")
        if folder_path:
            try:
                # Get all files in the selected folder
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                if not files:
                    messagebox.showwarning("No Files Found", "The selected folder contains no files.")
                    return

                for file_name in files:
                    base_name, _ = os.path.splitext(file_name)
                    random_extension = create_random_extension()  # Generate a random extension
                    new_file_path = os.path.join(folder_path, f"{base_name}.{random_extension}")

                    os.rename(os.path.join(folder_path, file_name), new_file_path)

                messagebox.showinfo("Success", f"All files in '{folder_path}' have been renamed with random extensions.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("No Folder Selected", "Please select a folder to rename files with fake extensions.")

    # File Metadata Manipulation Functions
    def manipulate_metadata(self):
        """
        Select a folder and apply metadata manipulation, timestamp modification,
        and hiding techniques to all files within the folder.
        """
        folder_path = filedialog.askdirectory()
        if not folder_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder.")
            return

        # Process each file in the selected folder
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Step 1: Modify timestamps
                self.modify_file_timestamp(file_path)
                print(f"Timestamps updated for: {file_path}")

                # Step 2: Hide the file and set system attributes
                self.hide_file(file_path)
                self.set_system_attribute(file_path)

                # Step 3: Manipulate metadata (Linux only)
                if platform.system() == 'Linux' or os.name == 'posix':
                    self.manipulate_file_metadata(file_path, new_owner="nobody", new_group="nogroup")
                    print(f"Metadata manipulated for: {file_path}")
                else:
                    print("Metadata manipulation is not applicable on this platform. Skipping this step...")

        messagebox.showinfo("Success", "Anti-forensics techniques applied to the entire folder.")

    # Helper functions for manipulate_metadata() start
    def modify_file_timestamp(self, file_path):
        """
        Modify the creation, modification, and access timestamps of a file
        to a random time within the last 5 years.
        """
        try:
            start_date = datetime.now() - timedelta(days=5 * 365)
            end_date = datetime.now()
            random_date = start_date + (end_date - start_date) * random.random()
            timestamp = time.mktime(random_date.timetuple())

            # Update modified and accessed timestamps
            os.utime(file_path, (timestamp, timestamp))

            # Update created timestamp (Windows only)
            if platform.system() == 'Windows':
                import pywintypes
                import win32file
                
                handle = win32file.CreateFile(
                    file_path,
                    win32file.GENERIC_WRITE,
                    win32file.FILE_SHARE_WRITE,
                    None,
                    win32file.OPEN_EXISTING,
                    win32file.FILE_ATTRIBUTE_NORMAL,
                    None,
                )
                created_time = pywintypes.Time(random_date)
                win32file.SetFileTime(handle, created_time, None, None)
                handle.close()
                print(f"Created timestamp updated for {file_path}.")
            else:
                print(f"Only modified and accessed timestamps updated for: {file_path}. Creation timestamp is not supported on this platform.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to modify timestamps: {e}")

    def manipulate_file_metadata(self, file_path, new_owner, new_group):
        """
        Manipulate file metadata by changing owner and group to random values.
        This works for both Linux and Windows platforms.
        """
        try:
            # Check platform and change ownership accordingly
            if platform.system() == 'Linux' or os.name == 'posix':
                os.system(f"chown {new_owner}:{new_group} {file_path}")
                print(f"Metadata for {file_path} changed to owner: {new_owner}, group: {new_group}.")
            elif platform.system() == 'Windows':
                # Windows doesn't have native support for changing owner/group, so we'll log random values
                print(f"Windows system: Fake owner: {new_owner}, Fake group: {new_group} applied to {file_path}.")
            else:
                print(f"Unsupported platform for metadata manipulation. Skipping for {file_path}.")
        except Exception as e:
            print(f"Error manipulating metadata for {file_path}: {e}")
            
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

    def set_system_attribute(self, file_path):
        """
        Set both 'Hidden' and 'System' attributes for the file (Windows only).
        """
        try:
            if platform.system() == 'Windows':
                # Set both Hidden (+h) and System (+s) attributes
                os.system(f'attrib +h +s "{file_path}"')  # Adding both Hidden and System attributes
                print(f"Hidden and System attributes set for: {file_path}")
            else:
                print(f"Setting Hidden and System attributes is not applicable on this platform.")
        except Exception as e:
            print(f"Error setting Hidden and System attributes for {file_path}: {e}")
    # Helper functions for manipulate_metadata() end
    
# Run the application
if __name__ == "__main__":
    # Default directory path for operations
    default_directory = "test_folder"

    # Define possible activities for fake activity injection
    global activities
    activities = ["login", "logout", "file_access", "system_shutdown"]

    # Ensure the default directory exists
    if not os.path.exists(default_directory):
        os.makedirs(default_directory)
    root = tk.Tk()
    app = ForensicsDisruptorApp(root)
    root.mainloop()
