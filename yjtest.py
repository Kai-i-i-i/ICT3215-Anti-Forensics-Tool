import os
import time
import random
from datetime import datetime, timedelta
import platform
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)

def create_encrypted_similar_file(original_file_path, content="Sensitive information."):
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
    confidential_file_name = os.path.splitext(original_file_name)[0] + "_confidential" + os.path.splitext(original_file_name)[1]
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

def generate_random_timestamp():
    """
    Generate a random timestamp within the last 5 years.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)  # Approximately 5 years ago
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def modify_file_timestamp(file_path, new_time=None):
    """
    Modify the access and modification time of a file.
    If new_time is None, generate a random timestamp.
    """
    if new_time is None:
        new_time = generate_random_timestamp()

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

# Define the folder to apply the anti-forensics techniques
target_folder = r"C:\Users\gohyu\Documents\GIt\ICT3215-Anti-Forensics-Tool\test_folder"

# Iterate over all files in the target folder and subfolders
for root, dirs, files in os.walk(target_folder):
    for filename in files:
        original_file_path = os.path.join(root, filename)
        
        print(f"\nProcessing original file: {original_file_path}")
        
        # Step 1: Create a similar encrypted file with "_confidential" in the name, or use the original if it already ends with "_confidential"
        confidential_file_path = create_encrypted_similar_file(original_file_path, content="Classified details about Project X.")
        
        # Step 2: Hide the original file
        hide_file(original_file_path)
        
        # Step 3: Apply random timestamp modification to the new confidential file or existing one if already "_confidential"
        if confidential_file_path:
            modify_file_timestamp(confidential_file_path)
            
            # Step 4: Attempt to manipulate metadata (Linux-only)
            manipulate_file_metadata(confidential_file_path, new_owner="nobody", new_group="nogroup")
