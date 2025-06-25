#!/usr/bin/env python3
"""
Twitter Bot - Main Entry Point

This script provides a command-line interface to:
1. Test the bot connections
2. Generate and post content manually
3. Start the automatic scheduler
4. View posting history
"""

import argparse
import sys
import signal
import time
from bot import TwitterBot
from scheduler import BotScheduler

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Twitter Bot for automated posting")
    parser.add_argument('command', choices=['test', 'post', 'schedule', 'history'], 
                       help='Command to execute')
    parser.add_argument('--context', choices=['general', 'project', 'thought', 'tip', 'question', 'sf_scene', 'student_perspective', 'building_moment'],
                       help='Context type for post generation')
    parser.add_argument('--dry-run', action='store_true',
                       help='Generate content without posting to Twitter')
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of history entries to show')
    
    args = parser.parse_args()
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        if args.command == 'test':
            print("Testing bot connections...")
            bot = TwitterBot()
            success = bot.test_connection()
            print("✅ All connections working!" if success else "❌ Connection test failed")
            
        elif args.command == 'post':
            print("Generating and posting content...")
            bot = TwitterBot()
            result = bot.generate_and_post(
                context_type=args.context,
                dry_run=args.dry_run
            )
            
            if result:
                if args.dry_run:
                    print(f"Generated content: {result['content']}")
                else:
                    print(f"✅ Tweet posted successfully!")
                    print(f"URL: {result.get('url', 'N/A')}")
            else:
                print("❌ Failed to generate or post content")
                
        elif args.command == 'schedule':
            print("Starting automated scheduler...")
            scheduler = BotScheduler()
            
            # Test connection first
            if not scheduler.bot.test_connection():
                print("❌ Connection test failed. Please check your configuration.")
                return
            
            scheduler.start()
            
            print("\n🤖 Bot is now running automatically!")
            print("Scheduled times:", scheduler.config.POSTING_SCHEDULE)
            print("Next run:", scheduler.next_run_time())
            print("\nPress Ctrl+C to stop...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop()
                print("\nBot stopped.")
                
        elif args.command == 'history':
            print(f"Showing last {args.limit} posts...")
            bot = TwitterBot()
            history = bot.get_post_history(args.limit)
            
            if not history:
                print("No posting history found.")
                return
            
            for i, post in enumerate(reversed(history), 1):
                print(f"\n{i}. {post['timestamp']}")
                print(f"   Type: {post['context_type']}")
                print(f"   Content: {post['content']}")
                print(f"   URL: {post['url']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 