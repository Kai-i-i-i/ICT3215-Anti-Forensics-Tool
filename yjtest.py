import os
import time
from datetime import datetime
import platform
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)

def create_encrypted_fake_file(file_path, content="Sensitive information."):
    """
    Create a fake file and encrypt its content. If the file already exists, replace it.
    """
    try:
        # Check if the file exists and delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Existing file {file_path} deleted.")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Encrypt the content and write it to the file
        encrypted_content = cipher.encrypt(content.encode())
        with open(file_path, 'wb') as fake_file:
            fake_file.write(encrypted_content)
        print(f"Encrypted fake file created at {file_path}. Content is misleading and encrypted.")
    except PermissionError:
        print(f"Permission denied: Unable to create or write to the file at {file_path}.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

def modify_file_timestamp(file_path, new_time):
    """
    Modify the access and modification time of a file.
    new_time should be in the format 'YYYY-MM-DD HH:MM:SS'
    """
    try:
        time_struct = time.strptime(new_time, '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(time_struct)
        os.utime(file_path, (timestamp, timestamp))
        print(f"Timestamps for {file_path} modified to {new_time}.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Cannot modify timestamp.")
    except Exception as e:
        print(f"An error occurred while modifying the timestamp: {e}")

def hide_file(file_path):
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

def manipulate_file_metadata(file_path, new_owner="fake_user", new_group="fake_group"):
    """
    Manipulate file metadata (requires root/administrator privileges on some systems).
    """
    if platform.system() == 'Linux':
        os.system(f"chown {new_owner}:{new_group} {file_path}")
        print(f"Owner and group of {file_path} changed to {new_owner}:{new_group}.")
    else:
        print("Metadata manipulation is limited on this OS.")

def alter_real_file_metadata(file_path, timestamp="2023-01-01 12:00:00", owner="real_user", group="real_group"):
    """
    Alter metadata of a real file, such as timestamp and owner/group.
    """
    modify_file_timestamp(file_path, timestamp)
    manipulate_file_metadata(file_path, new_owner=owner, new_group=group)

# Usage example
fake_file_path = r"C:\Users\gohyu\Documents\GIt\ICT3215-Anti-Forensics-Tool\confidential_report.txt"
real_file_path = r"C:\Users\gohyu\Documents\GIt\ICT3215-Anti-Forensics-Tool\real_important_file.txt"

# Step 1: Create an encrypted fake file (replaces it if it already exists)
create_encrypted_fake_file(fake_file_path, content="Classified details about Project X.")

# Step 2: Modify the file timestamp of the fake file to make it appear older
modify_file_timestamp(fake_file_path, "2022-06-15 08:30:00")

# Step 3: Hide the **real** file instead of the fake one
hide_file(real_file_path)

# Step 4: Manipulate metadata of the fake file (Linux-only example)
manipulate_file_metadata(fake_file_path, new_owner="nobody", new_group="nogroup")

# Step 5: Ensure real file exists and modify its metadata
if not os.path.exists(real_file_path):
    with open(real_file_path, 'w') as real_file:
        real_file.write("Important content.")
    print(f"Placeholder for real file created at {real_file_path}")

alter_real_file_metadata(real_file_path, timestamp="2020-05-20 14:00:00", owner="admin", group="admins")
