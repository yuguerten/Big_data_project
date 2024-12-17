from youtube_collector import YouTubeCommentCollector
from sentiment_analyzer import SentimentAnalyzer
import pandas as pd

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com' in url:
        return url.split('v=')[1].split('&')[0]
    return url

def main():
    # Initialize YouTube collector
    api_key = 'AIzaSyA8W-97TUc2_0R-IAq3mJU2G0hEAekPcyc'
    collector = YouTubeCommentCollector(api_key)
    
    # Convert YouTube URLs to video IDs
    youtube_urls = [
        "https://youtu.be/ovtz7__1UrI?si=mnNJvQvYS0yu-i6q"
    ]
    video_ids = [extract_video_id(url) for url in youtube_urls]
    
    # Collect comments
    all_comments = []
    for video_id in video_ids:
        comments_df = collector.get_video_comments(video_id)
        all_comments.append(comments_df)
    
    # Combine all pandas DataFrames
    combined_df = pd.concat(all_comments[:2], ignore_index=True)
    
    # Initialize sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Convert pandas DataFrame to Spark DataFrame and analyze
    spark_df = analyzer.spark.createDataFrame(combined_df)
    results = analyzer.analyze_comments(spark_df)
    
    # Show results
    results = results.select("text", "sentiment")
    
    # Calculate sentiment distribution
    # sentiment_counts = results.groupBy("sentiment").count()
    # sentiment_counts.show()

    # Save sentiment distribution to CSV
    results.write.mode("overwrite") \
        .option("header", "true") \
        .csv("/home/yuguerten/studies/Semestre_3/Big_data_2/projet/output/res.csv")

if __name__ == "__main__":
    main()
