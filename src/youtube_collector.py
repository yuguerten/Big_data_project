from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pandas as pd
import os

pd.DataFrame.iteritems = pd.DataFrame.items

class YouTubeCommentCollector:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key, static_discovery=False)

    def get_video_comments(self, video_id, max_results=100):
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results
            )
            
            while request:
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'date': comment['publishedAt'],
                        'likes': comment['likeCount'],
                    })
                
                request = self.youtube.commentThreads().list_next(request, response)
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
        return pd.DataFrame(comments)

    def save_to_csv(self, comments_df, output_path):
        comments_df.to_csv(output_path, index=False)
