import os
import sys
import json

def set_file_date(html_file):
	# Replace .html with .json to get the corresponding JSON file
	json_file = html_file.replace('.html', '.json')

	if not os.path.exists(json_file):
		print(f"Warning: JSON file not found for {html_file}, skipping")
		return

	with open(json_file) as f:
		data = json.load(f)
		# Use userEditedTimestampUsec (last edited time) as the file timestamp
		# This is in microseconds, so divide by 1,000,000 to get seconds
		edited_timestamp_usec = data.get('userEditedTimestampUsec', 0)
		created_timestamp_usec = data.get('createdTimestampUsec', 0)
		timestamp_usec = max(edited_timestamp_usec, created_timestamp_usec)
		if timestamp_usec:
			timestamp = timestamp_usec / 1000000.0
			os.utime(html_file, (timestamp, timestamp))
		else:
			print(f"Warning: No timestamp found in {json_file}")

for arg in sys.argv[1:]:
	if not ".html" in arg:
		continue
	set_file_date(arg)
