from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.linalg import Vectors
from pyspark.sql import Row

# Initialize Spark session
spark = SparkSession.builder \
    .appName("PySparkLogisticRegression") \
    .getOrCreate()

# Create a dummy dataset
data = [
    Row(label=1.0, features=Vectors.dense(1.0, 2.0, 3.0)),
    Row(label=0.0, features=Vectors.dense(2.0, 1.0, 0.0)),
    Row(label=0.0, features=Vectors.dense(3.0, 3.0, 3.0)),
    Row(label=1.0, features=Vectors.dense(0.0, 2.0, 1.0))
]

df = spark.createDataFrame(data)

# Train logistic regression model
lr = LogisticRegression(maxIter=10)
model = lr.fit(df)

# Print the model coefficients
print("Coefficients:", model.coefficients)
print("Intercept:", model.intercept)

# Stop Spark session
spark.stop()
