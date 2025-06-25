import json
import random
from typing import Dict, List
from openai import OpenAI
from config import Config

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.user_context = self._load_user_context()
    
    def _load_user_context(self) -> Dict:
        """Load user context from JSON file"""
        try:
            with open('user_context.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("user_context.json not found. Please create it with your profile information.")
    
    def _create_system_prompt(self) -> str:
        """Create a system prompt based on user context"""
        profile = self.user_context['profile']
        preferences = self.user_context['posting_preferences']
        
        return f"""You are a Twitter bot posting on behalf of {profile['name']}.

PROFILE:
- Bio: {profile['bio']}
- Profession: {profile['profession']}
- Location: {profile['location']}
- Interests: {', '.join(profile['interests'])}
- Writing style: {profile['writing_style']}

POSTING PREFERENCES:
- Tone: {preferences['tone']}
- Avoid topics: {', '.join(preferences['topics_to_avoid'])}
- Preferred hashtags: {', '.join(preferences['preferred_hashtags'])}
- Include questions: {preferences['include_questions']}
- Include tips: {preferences['include_tips']}

INSTRUCTIONS:
- Create authentic tweets that sound like the person described above
- Keep tweets under 280 characters
- Be engaging and valuable to followers
- Occasionally ask questions to encourage engagement
- Share insights, tips, or thoughts related to their interests
- Use a natural, conversational tone
- Don't be overly promotional
- Include relevant hashtags when appropriate (max 2-3 per tweet)

Generate tweets about current projects, recent thoughts, industry insights, or general musings that align with this person's interests and style."""
    
    def generate_tweet_content(self, context_type: str = "general") -> str:
        """Generate tweet content using OpenAI"""
        system_prompt = self._create_system_prompt()
        
        # Create context-specific user prompts
        user_prompts = {
            "general": "Create an engaging tweet about something interesting happening in AI, startups, or tech. Make it personal and authentic to a CS student's perspective.",
            "project": f"Create a tweet about building in public - share progress, learnings, or behind-the-scenes moments from one of these projects: {self.user_context.get('current_projects', [])}",
            "thought": f"Create a thoughtful tweet based on one of these recent observations or learnings: {', '.join(self.user_context.get('recent_thoughts', []))}",
            "tip": "Share a practical tip or insight about coding, AI, startups, or scaling tech - something useful for other builders and students.",
            "question": "Ask an engaging question about startup challenges, AI applications, tech scaling, or the founder journey that would spark interesting discussion.",
            "sf_scene": "Share an observation or takeaway from the San Francisco startup scene - maybe something learned from a founder meeting, event, or just being immersed in the ecosystem.",
            "student_perspective": "Share a unique insight that comes from being a CS student who's also deeply involved in the startup world - bridging theory and practice.",
            "building_moment": "Share a behind-the-scenes moment from building projects - a breakthrough, challenge, or interesting technical decision."
        }
        
        user_prompt = user_prompts.get(context_type, user_prompts["general"])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            tweet_content = response.choices[0].message.content.strip()
            
            # Ensure tweet is within character limit
            if len(tweet_content) > Config.MAX_TWEET_LENGTH:
                tweet_content = tweet_content[:Config.MAX_TWEET_LENGTH - 3] + "..."
            
            return tweet_content
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def get_random_context_type(self) -> str:
        """Get a random context type for varied content"""
        context_types = ["general", "project", "thought", "tip", "question", "sf_scene", "student_perspective", "building_moment"]
        # Weight certain types more heavily for authentic content
        weighted_types = (
            ["thought"] * 3 +  # More thoughts/observations
            ["project", "building_moment"] * 2 +  # Building in public
            ["tip", "question"] * 2 +  # Valuable content
            ["sf_scene", "student_perspective"] +  # Unique perspectives
            ["general"]
        )
        return random.choice(weighted_types) 