from multiprocessing import Pool
from collections import defaultdict
import os

# Mapper function
def mapper(chunk):
    mapped_data = []
    for line in chunk:
        parts = line.strip().split()
        if len(parts) > 0:
            ip = parts[0]  # Extract the IP address
            mapped_data.append((ip, 1))
    return mapped_data

# Reducer function
def reducer(mapped_data):
    reduced_data = defaultdict(int)
    for ip, count in mapped_data:
        reduced_data[ip] += count
    return reduced_data

# Combiner function to merge results from different reducers
def combine_reduced_results(reduced_results):
    final_result = defaultdict(int)
    for partial_result in reduced_results:
        for ip, count in partial_result.items():
            final_result[ip] += count
    return final_result

# Function to split the data into chunks
def chunkify(data, n_chunks):
    chunk_size = max(1, len(data) // n_chunks)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Parallel MapReduce execution
def parallel_mapreduce(file_path, n_processes):
    try:
        with open(file_path, 'r') as f:
            data = f.readlines()

        # Split data into chunks for parallel processing
        chunks = chunkify(data, n_processes)

        # Create a pool of workers
        with Pool(n_processes) as pool:
            # Map step: Process chunks in parallel
            mapped_results = pool.map(mapper, chunks)

            # Combine all mapped results into a single list
            combined_mapped = [item for sublist in mapped_results for item in sublist]

            # Reduce step: Group by IP and reduce in parallel
            grouped_data = defaultdict(list)
            for ip, count in combined_mapped:
                grouped_data[ip].append(count)

            # Reduce grouped data in parallel
            reduced_results = pool.map(
                lambda item: {item[0]: sum(item[1])}, grouped_data.items()
            )

        # Combine reduced results from all processes
        final_result = combine_reduced_results(reduced_results)
        return final_result

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Run the MapReduce simulation
if __name__ == "__main__":
    n_processes = min(4, os.cpu_count())  # Use up to 4 processes or the CPU count
    file_path = os.path.join(os.getcwd(), "map_reduce", "weblog.txt")  # Path to your web log file

    print("Processing the web logs using parallel MapReduce...")
    result = parallel_mapreduce(file_path, n_processes)

    if result:
        print("\nTotal requests per IP address:")
        for ip, count in result.items():
            print(f"{ip}: {count}")
    else:
        print("No data processed.")
