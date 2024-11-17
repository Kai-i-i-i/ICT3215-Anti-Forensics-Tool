import win32evtlogutil
import win32evtlog

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

create_forged_event()
