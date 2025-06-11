from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

# Step 1: Initialize Spark Session
spark = SparkSession.builder \
    .appName("TV Marketing Analysis") \
    .getOrCreate()

# Step 2: Load the dataset
df = spark.read.csv("tvmarketing.csv", header=True, inferSchema=True)

# Step 3: Inspect the data
df.printSchema()
df.show(5)

# Step 4: Prepare the feature vector
assembler = VectorAssembler(inputCols=["TV"], outputCol="features")
df_features = assembler.transform(df)

# Step 5: Train/Test split
train_data, test_data = df_features.randomSplit([0.8, 0.2], seed=42)

# Step 6: Define and fit the Linear Regression model
lr = LinearRegression(featuresCol="features", labelCol="Sales")
lr_model = lr.fit(train_data)

# Step 7: Print model coefficients
print(f"Coefficient: {lr_model.coefficients}")
print(f"Intercept: {lr_model.intercept}")

# Step 8: Make predictions
predictions = lr_model.transform(test_data)
predictions.select("TV", "Sales", "prediction").show(5)

# Step 9: Evaluate the model
evaluator = RegressionEvaluator(
    labelCol="Sales", predictionCol="prediction", metricName="rmse"
)
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE): {rmse:.3f}")

# Optional: R-squared
r2 = lr_model.summary.r2
print(f"R-squared: {r2:.3f}")

# Stop the Spark session
spark.stop()
