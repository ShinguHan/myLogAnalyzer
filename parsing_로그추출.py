# Finalize the code

import csv
import re
from datetime import datetime
import pprint

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

# Print the log_info
for info in log_info:
    pprint.pprint(info)
