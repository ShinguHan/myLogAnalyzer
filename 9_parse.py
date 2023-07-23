# Import the re module
import re
import pprint
import csv
from datetime import datetime

# Re-run the standard file parsing code

# Read the standard file
with open("st.md", "r", encoding="utf-8") as f:
    standard_content = f.readlines()

# Parse the standard file
standard_info = []
for line in standard_content:
    # Find the participant, direction, and message in the line
    match = re.search(r"(cv|mc) ->> (cv|mc) : (S\d+F\d+)", line)
    if match:
        participant1, participant2, message = match.groups()
        # Find the CEID in the line, if it exists
        ceid_match = re.search(r"(CEID = \d+)", line)
        ceid = ceid_match.group() if ceid_match else None
        # Store the information
        standard_info.append((participant1, participant2, message, ceid))

# Print the parsed standard file
pprint.pprint(standard_info)


# Define the parsing function
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

    # Sort the log_info by time
    log_info.sort()

    return log_info


# Parse the log file
log_info = parse_log_file("co.csv")
pprint.pprint(log_info)

# Check if the log info follows the standard sequence
for i, (time, direction, message, detail) in enumerate(log_info):
    # Check if the message is in the standard sequence
    if i < len(standard_info):
        std_participant1, std_participant2, std_message, std_ceid = standard_info[i]
        log_participant1 = "cv" if direction == "->>" else "mc"
        log_participant2 = "mc" if direction == "->>" else "cv"

        # If the message does not match the standard sequence, print an error
        if (log_participant1, log_participant2, message) != (
            std_participant1,
            std_participant2,
            std_message,
        ):
            print(f"Error: Log item at {time} does not match the standard sequence")
            print(
                f"Expected: {std_participant1} ->> {std_participant2} : {std_message}"
            )
            print(f"Got: {log_participant1} ->> {log_participant2} : {message}")
            print("Detail:", detail)
            print()

        # If the CEID does not match the standard sequence, print an error
        if std_ceid:
            log_ceid_match = re.search(r"(CEID = \d+)", detail)
            log_ceid = log_ceid_match.group() if log_ceid_match else None
            if log_ceid != std_ceid:
                print(
                    f"Error: CEID of log item at {time} does not match the standard sequence"
                )
                print(f"Expected: {std_ceid}")
                print(f"Got: {log_ceid}")
                print("Detail:", detail)
                print()

    # If the log info has more messages than the standard sequence, print an error
    else:
        print(f"Error: Log item at {time} is not in the standard sequence")
        print(f"Got: {log_participant1} ->> {log_participant2} : {message}")
        print("Detail:", detail)
        print()
