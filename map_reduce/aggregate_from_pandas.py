import pandas as pd
from collections import defaultdict

# Sample sales data in a DataFrame
data = {
    'Product': ['Apple', 'Banana', 'Apple', 'Banana', 'Orange', 'Banana', 'Apple', 'Orange'],
    'Sales': [100, 150, 200, 250, 300, 100, 150, 200]
}

df = pd.DataFrame(data)

# Display the DataFrame
print("Original DataFrame:")
print(df)

# Map function: Convert each row into key-value pair (Product, Sales)
def map_function(row):
    product = row['Product']
    sales = row['Sales']
    return product, sales

# Shuffle and Sort: Group all key-value pairs by key (Product)
def shuffle_sort(mapped_data):
    grouped_data = defaultdict(list)
    for product, sales in mapped_data:
        grouped_data[product].append(sales)
    return grouped_data

# Reduce function: Sum the sales for each product
def reduce_function(grouped_data):
    reduced_data = {product: sum(sales) for product, sales in grouped_data.items()}
    return reduced_data

# Simulate the MapReduce process on a DataFrame
def map_reduce(df):
    # Step 1: Map Phase
    mapped_data = []
    for _, row in df.iterrows():
        mapped_data.append(map_function(row))
    
    # Step 2: Shuffle/Sort Phase
    grouped_data = shuffle_sort(mapped_data)
    
    # Step 3: Reduce Phase
    reduced_data = reduce_function(grouped_data)
    
    return reduced_data

# Running the MapReduce aggregation on the sales data
result = map_reduce(df)

# Display the result
print("\nAggregated Sales Data using MapReduce:")
for product, total_sales in result.items():
    print(f"{product}: {total_sales}")
