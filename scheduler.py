import schedule
import time
import threading
from datetime import datetime
from bot import TwitterBot
from config import Config

class BotScheduler:
    def __init__(self):
        self.bot = TwitterBot()
        self.config = Config()
        self.running = False
        self.thread = None
        
    def setup_schedule(self):
        """Setup posting schedule based on configuration"""
        posting_times = self.config.POSTING_SCHEDULE.split(',')
        
        for time_str in posting_times:
            time_str = time_str.strip()
            print(f"Scheduling daily post at {time_str}")
            schedule.every().day.at(time_str).do(self.scheduled_post)
    
    def scheduled_post(self):
        """Execute a scheduled post"""
        print(f"Executing scheduled post at {datetime.now()}")
        try:
            result = self.bot.generate_and_post()
            if result:
                print(f"Scheduled post successful: {result.get('url', 'N/A')}")
            else:
                print("Scheduled post failed")
        except Exception as e:
            print(f"Error in scheduled post: {e}")
    
    def start(self):
        """Start the scheduler in a separate thread"""
        if self.running:
            print("Scheduler is already running")
            return
        
        self.setup_schedule()
        self.running = True
        
        def run_scheduler():
            print("Bot scheduler started...")
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        self.thread = threading.Thread(target=run_scheduler, daemon=True)
        self.thread.start()
        print("Scheduler thread started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Scheduler stopped")
    
    def next_run_time(self):
        """Get the next scheduled run time"""
        jobs = schedule.jobs
        if jobs:
            next_job = min(jobs, key=lambda job: job.next_run)
            return next_job.next_run
        return None
    
    def list_scheduled_jobs(self):
        """List all scheduled jobs"""
        jobs = []
        for job in schedule.jobs:
            jobs.append({
                "job": str(job),
                "next_run": job.next_run,
                "tags": job.tags
            })
        return jobs 