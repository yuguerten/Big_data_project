from pyspark.sql import SparkSession
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import numpy as np

def analyze_sentiment_standalone(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment_score = predictions.detach().numpy()[0]
    sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
    return sentiment_map[np.argmax(sentiment_score)]

# Initialize SparkSession
spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .appName("Sentiment analysis") \
    .getOrCreate()

# Path to the CSV in HDFS
hdfs_path = "hdfs://namenode:9000/user/data/youtube_comments.csv"

# Read CSV from HDFS
df = spark.read.csv(hdfs_path, header=True)

# Initialize sentiment analysis model
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

# Create UDF for sentiment analysis
sentiment_udf = udf(lambda text: analyze_sentiment_standalone(text, tokenizer, model), StringType())

# Apply sentiment analysis
results = df.withColumn("sentiment", sentiment_udf("text"))

# Show results
results.select("text", "sentiment").show(truncate=False)

# Count sentiments
sentiment_counts = results.groupBy("sentiment").count()
sentiment_counts.show()

# Save results to HDFS
results.write.mode("overwrite") \
    .option("header", "true") \
    .csv("hdfs://namenode:9000/user/data/youtube_comments_sentiment")

# Save sentiment counts to HDFS
sentiment_counts.write.mode("overwrite") \
    .option("header", "true") \
    .csv("hdfs://namenode:9000/user/data/sentiment_counts")

# Stop SparkSession
spark.stop()

