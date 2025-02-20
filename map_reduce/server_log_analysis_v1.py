'''
Problem Statement:

We have a web server log file in a standard format (e.g., Apache access logs). 
Each line represents a single request, and we want to count how many requests 
were made by each IP address.

Steps:
    Mapper: Parse each log line and emit key-value pairs where the key is the IP address and the value is 1.
    Shuffle and Sort: Group all key-value pairs by key (IP address).
    Reducer: Sum up all values for each key to get the total number of requests per IP.
    
'''

import re
from multiprocessing import Pool
from collections import defaultdict
from itertools import groupby

# Sample log lines
log_lines = [
    '192.168.0.1 - - [27/Jan/2025:10:00:00] "GET /index.html HTTP/1.1" 200 1024',
    '192.168.0.2 - - [27/Jan/2025:10:01:00] "GET /about.html HTTP/1.1" 200 2048',
    '192.168.0.1 - - [27/Jan/2025:10:02:00] "GET /contact.html HTTP/1.1" 404 512',
    '192.168.0.3 - - [27/Jan/2025:10:03:00] "POST /submit HTTP/1.1" 200 256',
    '192.168.0.2 - - [27/Jan/2025:10:04:00] "GET /index.html HTTP/1.1" 200 1024',
    '192.168.0.1 - - [27/Jan/2025:10:05:00] "GET /index.html HTTP/1.1" 200 1024'
]

# Regex to extract IP address from log line
log_pattern = re.compile(r'^(\d+\.\d+\.\d+\.\d+)')

# Mapper function
def map_log_line(line):
    match = log_pattern.match(line)
    if match:
        ip = match.group(1)
        return (ip, 1)  # Emit (IP, 1)
    return None

# Reducer function
def reduce_grouped_data(grouped_data):
    result = {}
    for ip, occurrences in grouped_data.items():
        result[ip] = sum(occurrences)  # Sum all occurrences for each IP
    return result

# Main function
def map_reduce(log_lines):
    # Step 1: Map
    with Pool() as pool:
        mapped_data = pool.map(map_log_line, log_lines)

    # Filter out None values (invalid log lines)
    mapped_data = [item for item in mapped_data if item]

    # Step 2: Shuffle and Sort (Group by IP)
    grouped_data = defaultdict(list)
    for key, value in mapped_data:
        grouped_data[key].append(value)

    # Step 3: Reduce
    reduced_data = reduce_grouped_data(grouped_data)

    return reduced_data

# Run MapReduce
if __name__ == "__main__":
    result = map_reduce(log_lines)
    print("IP Address Request Counts:")
    for ip, count in result.items():
        print(f"{ip}: {count}")
