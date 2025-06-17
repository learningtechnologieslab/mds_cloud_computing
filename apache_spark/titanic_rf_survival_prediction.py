import os
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline

# Resolve base directory of this script
base_dir = os.path.abspath(os.path.dirname(__file__))

# Construct full input and output paths
input_path = f"file://{os.path.join(base_dir, 'titanic.csv')}"
output_path = os.path.join(base_dir, "output.txt")

# Step 1: Initialize Spark session
spark = SparkSession.builder.appName("TitanicRandomForest").getOrCreate()

# Step 2: Load dataset
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Step 3: Drop unnecessary columns
df = df.drop("Name", "Cabin", "Ticket", "PassengerId")

# Step 4: Drop rows with null values
df = df.dropna()

# Step 5: Encode categorical variables
sex_indexer = StringIndexer(inputCol="Sex", outputCol="SexIndexed")
embarked_indexer = StringIndexer(inputCol="Embarked", outputCol="EmbarkedIndexed")

# Step 6: Assemble features
assembler = VectorAssembler(
    inputCols=["Pclass", "SexIndexed", "Age", "SibSp", "Parch", "Fare", "EmbarkedIndexed"],
    outputCol="features"
)

# Step 7: Create Random Forest model
rf = RandomForestClassifier(labelCol="Survived", featuresCol="features", numTrees=100)

# Step 8: Build pipeline
pipeline = Pipeline(stages=[sex_indexer, embarked_indexer, assembler, rf])

# Step 9: Train-test split
train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)

# Step 10: Train model
model = pipeline.fit(train_data)

# Step 11: Predict
predictions = model.transform(test_data)

# Step 12: Evaluate
evaluator = MulticlassClassificationEvaluator(labelCol="Survived", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

# Write accuracy to output file
with open(output_path, "w") as f:
    f.write(f"Random Forest Classification Accuracy: {accuracy:.4f}\n")

# Stop Spark
spark.stop()
