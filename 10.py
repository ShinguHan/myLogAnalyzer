# 되는 하는데 로그 파일쪽 정보를 취합하고 있음

# First, let's parse the standard and log files again using the provided python code
# To do this, we'll need to adapt the code to use the new file paths and to return the parsed data instead of printing it

# Import the required modules
import re
import csv
from datetime import datetime
import pprint


# Parse the standard file
def parse_standard_file(standard_file_path):
    with open(standard_file_path, "r", encoding="utf-8") as f:
        standard_content = f.readlines()

    standard_info = []
    for line in standard_content:
        match = re.search(r"(cv|mc) ->> (cv|mc) : (S\d+F\d+)", line)
        if match:
            participant1, participant2, message = match.groups()
            ceid_match = re.search(r"(CEID = \d+)", line)
            ceid = ceid_match.group() if ceid_match else None
            standard_info.append((participant1, participant2, message, ceid))

    return standard_info


# Parse the log file
def parse_log_file(log_file_path):
    # Read the log file
    with open("co.csv", "r", encoding="utf-8") as f:
        log_content = f.readlines()

    # List to store the parsed log information
    log_info = []

    # Parse each line in the log file
    fields = []
    detail = ""
    for line in log_content:
        # Use the csv module to correctly split the line into fields
        reader = csv.reader([line])
        new_fields = list(reader)[0]

        # If the line starts with "Com", process the previous log item and start a new one
        if new_fields[0] in ["Com", "Info", "Error", "Debug"] and fields:
            try:
                # Only process the "Com" log items
                if fields[0] == "Com":
                    # Extract the needed information
                    time_str = fields[2]
                    direction = "->>" if "-->" in fields[8] else "<<-"

                    # Find the message pattern, if it exists
                    message_match = re.search("S\\d+F\\d+", fields[9])
                    message = message_match.group() if message_match else ""

                    # Convert the time information to a datetime object
                    time = datetime.strptime(time_str, "%d-%b-%Y %H:%M:%S:%f")

                    # Store the information
                    log_info.append((time, direction, message, detail))
            except Exception as e:
                print(f"Failed to process log item: {e}")
                print("Fields:", fields)

            # Start a new log item
            fields = new_fields
            detail = ""
        else:
            # Otherwise, accumulate the fields
            fields.extend(new_fields[:-1])
            # Concatenate the detail
            detail += new_fields[-1]

    # Process the last log item
    if fields and fields[0] == "Com":
        try:
            # Extract the needed information
            time_str = fields[2]
            direction = "->>" if "-->" in fields[8] else "<<-"

            # Find the message pattern, if it exists
            message_match = re.search("S\\d+F\\d+", fields[8])
            message = message_match.group() if message_match else ""

            # Convert the time information to a datetime object
            time = datetime.strptime(time_str, "%d-%b-%Y %H:%M:%S:%f")

            # Store the information
            log_info.append((time, direction, message, detail))
        except Exception as e:
            print(f"Failed to process log item: {e}")
            print("Fields:", fields)

    log_info.sort()

    return log_info


# Parse the standard and log files
standard_info = parse_standard_file("st.md")
log_info = parse_log_file("co.csv")

pprint.pprint(standard_info)
pprint.pprint(log_info)

# Now we'll define some functions to check for missing and duplicate messages and cycle repetitions


# Check for missing messages
def check_missing_messages(standard_info, log_info):
    missing_messages = []

    # Convert the standard info to a set for faster lookup
    standard_messages = set((p1, p2, m) for p1, p2, m, c in standard_info)

    # Check each log message
    for time, direction, message, detail in log_info:
        log_participant1 = "cv" if direction == "->>" else "mc"
        log_participant2 = "mc" if direction == "->>" else "cv"
        if (log_participant1, log_participant2, message) not in standard_messages:
            missing_messages.append((time, log_participant1, log_participant2, message))

    return missing_messages


# Check for duplicate messages
def check_duplicate_messages(log_info):
    duplicate_messages = []
    last_message = None

    # Check each log message
    for time, direction, message, detail in log_info:
        log_participant1 = "cv" if direction == "->>" else "mc"
        log_participant2 = "mc" if direction == "->>" else "cv"
        current_message = (log_participant1, log_participant2, message)
        if current_message == last_message:
            duplicate_messages.append(
                (time, log_participant1, log_participant2, message)
            )
        last_message = current_message

    return duplicate_messages


# Check for cycle repetitions
def check_cycle_repetitions(standard_info, log_info):
    cycle_repetitions = 0
    standard_index = 0

    # Check each log message
    for time, direction, message, detail in log_info:
        log_participant1 = "cv" if direction == "->>" else "mc"
        log_participant2 = "mc" if direction == "->>" else "cv"
        current_message = (log_participant1, log_participant2, message)
        standard_message = (
            standard_info[standard_index][0],
            standard_info[standard_index][1],
            standard_info[standard_index][2],
        )
        if current_message == standard_message:
            standard_index += 1
            if standard_index == len(standard_info):
                cycle_repetitions += 1
                standard_index = 0
        else:
            standard_index = 0

    return cycle_repetitions


# Check for missing messages, duplicate messages, and cycle repetitions
missing_messages = check_missing_messages(standard_info, log_info)
duplicate_messages = check_duplicate_messages(log_info)
cycle_repetitions = check_cycle_repetitions(standard_info, log_info)

pprint.pprint(
    [
        "missing_messages",
        missing_messages,
        "duplicate_messages",
        duplicate_messages,
        "cycle_repetitions",
        cycle_repetitions,
    ]
)
