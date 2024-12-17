from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pyspark.sql import SparkSession
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

class SentimentAnalyzer:
    def __init__(self):
        self.spark = SparkSession.builder.appName("YouTubeCommentAnalysis").getOrCreate()
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        
    def analyze_comments(self, spark_df):
        # Create a closure that doesn't include self
        tokenizer = self.tokenizer
        model = self.model
        
        def analyze_with_closure(text):
            return analyze_sentiment_standalone(text, tokenizer, model)
        
        # Register UDF with the closure
        sentiment_udf = udf(analyze_with_closure, StringType())
        
        # Apply sentiment analysis to text column
        result_df = spark_df.withColumn("sentiment", sentiment_udf("text"))
        return result_df
