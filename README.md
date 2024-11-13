# ICT3215-Anti-Forensics-Tool

# Forensics Disruptor

## Introduction
*Forensics Disruptor* is an advanced anti-forensics tool designed to actively disrupt digital forensic investigations. Unlike traditional anti-forensic tools that focus on hiding or deleting evidence, *Forensics Disruptor* injects false evidence, manipulates logs, and creates misleading data to confuse and mislead investigators. This tool is primarily developed for educational purposes, helping cybersecurity professionals test and hone their forensic analysis skills in real-world scenarios.

## Features
*Forensics Disruptor* automates several advanced anti-forensics techniques to disrupt forensic investigations:

1. **Log Forgery**: Modifies system and application logs to alter timestamps, inject false user activity, and mask unauthorized actions. This feature also includes log file poisoning to further mislead investigators.
2. **Phantom Files**: Generates fake files that appear legitimate but contain misleading or encrypted data, wasting investigators' time.
   - Includes features such as sparse files, in-memory files, hidden files, symbolic links, and NTFS Alternate Data Streams (ADS).
3. **File Metadata Manipulation**: Alters file attributes, visibility, and metadata to make files difficult to trace or verify.
4. **Cross-Platform Support**: The tool is primarily developed for Windows, but may include support for other operating systems.
5. **User Interface**: The tool provides a user-friendly graphical user interface (GUI) with both automatic and manual features.

## Requirements
- **Operating System**: Windows 10 or higher
- **Programming Language**: Python 3.8+
- **Dependencies**:
  - Refer to `requirements.txt`

## Usage

### Step 1: Clone the Repository
```bash
git clone https://github.com/Kai-i-i-i/ICT3215-Anti-Forensics-Tool.git
cd ICT3215-Anti-Forensics-Tool
```

### Step 2: Install Dependencies
Ensure you have Python 3.8+ installed on your system. Then, install the necessary Python packages:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Program
You can run the program by executing the main Python script:
```bash
python main.py
```

### GUI Overview
- **Log Forgery**: Automatically modifies system logs (e.g., altering timestamps, injecting fake user activity). Some functions are auto-executed upon startup, while others can be manually triggered via the GUI.
- **Phantom File Creation**: Creates fake files in critical system locations. These files may appear important but contain minimal data, be encrypted, or have altered metadata.
- **File Metadata Manipulation**: Allows you to manipulate file timestamps and attributes. This function lets you hide files in plain sight or make them harder to track.

### Example Commands (if running manually)
To create a phantom file:
```bash
python phantom_file.py --path "C:/Users/target_folder" --size 1024
```

To alter file metadata:
```bash
python metadata_manipulation.py --file "C:/Users/file.txt" --timestamp "2022-10-01 12:00:00"
```

## Features Breakdown

1. **Log Forgery**:
   - Alters log entries to inject false activities and replace unauthorized actions.
   - Uses log poisoning techniques to execute malicious code through HTTP GET requests.
   - Example: Using `Timestomp`-like functionality to modify log timestamps.

2. **Phantom Files**:
   - Creates fake files with realistic names and locations.
   - Includes features such as sparse files, in-memory files, and symbolic links.
   - Adds corrupted or locked files that cannot be opened, and files with fake extensions.

3. **File Metadata Manipulation**:
   - Changes the file creation, modification, and access times.
   - Hides files in obscure directories or modifies their metadata to mislead investigators.

## Testing

1. **Functional Testing**: Test the features in simulated forensic environments.
   - Run the tool, and then attempt to analyze the logs and files using common forensic tools such as [Autopsy](https://www.sleuthkit.org/autopsy/).
   - Ensure the tool misleads the investigator by altering logs, creating phantom files, and manipulating file metadata.

2. **Performance Testing**: Verify that the tool does not significantly degrade system performance.
   - Monitor CPU and memory usage while running intensive tasks such as file creation and log forgery.

## Known Issues
- The in-memory file feature is still under development and may not function optimally on all systems.
- Cross-platform support for Linux and macOS is currently limited; the tool is primarily tested on Windows.

## Future Development
- Improve cross-platform support, focusing on Linux-based forensic tools.
- Add more advanced file manipulation features, such as encrypting files with fake extensions.
- Expand the GUI to offer more customization options for users.

## Credits
- Resources: Timestomp (Metasploit), Autopsy, StegHide, OpenPuff
