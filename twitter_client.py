import tweepy
from typing import Optional
from config import Config

class TwitterClient:
    def __init__(self):
        self.config = Config()
        self.client = self._authenticate()
    
    def _authenticate(self) -> tweepy.Client:
        """Authenticate with Twitter API v2"""
        try:
            # Use API v2 Client with OAuth 1.0a for posting
            client = tweepy.Client(
                bearer_token=self.config.TWITTER_BEARER_TOKEN,
                consumer_key=self.config.TWITTER_CONSUMER_KEY,
                consumer_secret=self.config.TWITTER_CONSUMER_SECRET,
                access_token=self.config.TWITTER_ACCESS_TOKEN,
                access_token_secret=self.config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            
            # Test authentication by getting user info
            me = client.get_me()
            print(f"Twitter authentication successful! Logged in as: @{me.data.username}")
            return client
            
        except Exception as e:
            print(f"Twitter authentication failed: {e}")
            raise
    
    def post_tweet(self, content: str) -> Optional[dict]:
        """Post a tweet using API v2"""
        try:
            if len(content) > Config.MAX_TWEET_LENGTH:
                print(f"Tweet too long: {len(content)} characters")
                return None
            
            # Post the tweet using API v2
            response = self.client.create_tweet(text=content)
            
            if response.data:
                tweet_id = response.data['id']
                result = {
                    "id": tweet_id,
                    "text": content,
                    "created_at": "now",  # API v2 doesn't return created_at in response
                    "url": f"https://twitter.com/user/status/{tweet_id}"
                }
                
                print(f"Tweet posted successfully: {result['url']}")
                return result
            else:
                print("Tweet posting failed - no response data")
                return None
            
        except tweepy.TweepyException as e:
            print(f"Error posting tweet: {e}")
            if "403" in str(e):
                print("💡 This looks like an API access issue. You may need:")
                print("   1. Elevated access from Twitter Developer Portal")
                print("   2. Or upgrade to a paid Twitter API plan")
                print("   3. See: https://developer.twitter.com/en/portal/product")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_recent_tweets(self, count: int = 5) -> list:
        """Get recent tweets from authenticated user using API v2"""
        try:
            # Get authenticated user first
            me = self.client.get_me()
            user_id = me.data.id
            
            # Get user's tweets (API v2 requires min 5, max 100)
            tweets = self.client.get_users_tweets(
                id=user_id, 
                max_results=max(5, min(count, 10)),  # API v2 requires minimum 5
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if not tweets.data:
                return []
            
            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "retweet_count": tweet.public_metrics.get('retweet_count', 0),
                    "favorite_count": tweet.public_metrics.get('like_count', 0)
                }
                for tweet in tweets.data
            ]
        except Exception as e:
            print(f"Error fetching recent tweets: {e}")
            return [] 