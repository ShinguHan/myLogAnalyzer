# 이게 내가 원하는 형식으로 도출된 것

# Import the re module
import re
import pprint

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
