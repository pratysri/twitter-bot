import json
import logging
from datetime import datetime
from typing import Optional
from content_generator import ContentGenerator
from twitter_client import TwitterClient
from config import Config

class TwitterBot:
    def __init__(self):
        self.config = Config()
        self.config.validate_config()
        
        self.content_generator = ContentGenerator()
        self.twitter_client = TwitterClient()
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging for the bot"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_and_post(self, context_type: str = None, dry_run: bool = False) -> Optional[dict]:
        """Generate content and post to Twitter"""
        try:
            # Generate content
            if not context_type:
                context_type = self.content_generator.get_random_context_type()
            
            self.logger.info(f"Generating {context_type} content...")
            content = self.content_generator.generate_tweet_content(context_type)
            
            if not content:
                self.logger.error("Failed to generate content")
                return None
            
            self.logger.info(f"Generated content: {content}")
            
            if dry_run:
                self.logger.info("Dry run mode - not posting to Twitter")
                return {"content": content, "dry_run": True}
            
            # Post to Twitter
            result = self.twitter_client.post_tweet(content)
            
            if result:
                # Log the successful post
                self._log_post(content, result, context_type)
                self.logger.info(f"Successfully posted tweet: {result['url']}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in generate_and_post: {e}")
            return None
    
    def _log_post(self, content: str, result: dict, context_type: str):
        """Log successful posts to a file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "tweet_id": result["id"],
            "url": result["url"],
            "context_type": context_type
        }
        
        try:
            # Read existing logs
            try:
                with open('post_history.json', 'r') as f:
                    history = json.load(f)
            except FileNotFoundError:
                history = []
            
            # Add new entry
            history.append(log_entry)
            
            # Keep only last 100 posts
            history = history[-100:]
            
            # Write back to file
            with open('post_history.json', 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error logging post: {e}")
    
    def get_post_history(self, limit: int = 10) -> list:
        """Get recent post history"""
        try:
            with open('post_history.json', 'r') as f:
                history = json.load(f)
                return history[-limit:]
        except FileNotFoundError:
            return []
        except Exception as e:
            self.logger.error(f"Error reading post history: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test connections to both OpenAI and Twitter"""
        try:
            # Test OpenAI
            test_content = self.content_generator.generate_tweet_content("general")
            if not test_content:
                self.logger.error("OpenAI connection test failed")
                return False
            
            # Test Twitter (get recent tweets without posting)
            recent_tweets = self.twitter_client.get_recent_tweets(1)
            
            self.logger.info("All connections successful!")
            return True
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False 