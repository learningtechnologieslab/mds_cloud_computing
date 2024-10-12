from collections import defaultdict

# Sample input data: List of documents (strings)
documents = [
    "Hello world",
    "Hello MapReduce",
    "MapReduce makes big data processing simple",
    "The world of big data"
]

# Map function: Convert documents into key-value pairs (word, 1)
def map_function(doc):
    words = doc.split()
    key_value_pairs = [(word.lower(), 1) for word in words]
    return key_value_pairs

# Shuffle and Sort: Group all key-value pairs by key (word)
def shuffle_sort(mapped_data):
    grouped_data = defaultdict(list)
    for word, count in mapped_data:
        grouped_data[word].append(count)
    return grouped_data

# Reduce function: Sum the values for each word
def reduce_function(grouped_data):
    reduced_data = {word: sum(counts) for word, counts in grouped_data.items()}
    return reduced_data

# Simulate the MapReduce process
def map_reduce(documents):
    # Step 1: Map Phase
    mapped_data = []
    for doc in documents:
        mapped_data.extend(map_function(doc))
    
    # Step 2: Shuffle/Sort Phase
    grouped_data = shuffle_sort(mapped_data)
    
    # Step 3: Reduce Phase
    reduced_data = reduce_function(grouped_data)
    
    return reduced_data

# Running the MapReduce word count
result = map_reduce(documents)

# Display the result
print("Word Count using MapReduce:")
for word, count in result.items():
    print(f"{word}: {count}")
