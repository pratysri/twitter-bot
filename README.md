# Twitter Bot with OpenAI

An intelligent Twitter bot that posts on your behalf using OpenAI's GPT models. The bot learns from your context and generates authentic tweets that match your style and interests.

## 🐦 AI-Powered Twitter Bot — How It Works

This project is a fully automated, context-aware Twitter bot designed for authentic, engaging posting—powered by OpenAI's latest GPT-4.1 Mini model and the Twitter API.

### ✨ What It Does

- **Personalized Content Generation:**  
  Leverages your custom profile (student, SF startup scene, interests, writing style) to generate tweets that sound like you.
- **Contextual Awareness:**  
  Pulls from your current projects, recent thoughts, and unique perspectives to create relevant, timely posts.
- **Varied Content Types:**  
  Supports multiple tweet styles:  
  - Project/building-in-public updates  
  - Observations from the SF tech scene  
  - Student/founder insights  
  - Tips, questions, and more
- **Smart Prompting:**  
  Uses a weighted system to favor authentic, thoughtful, and "building in public" content.
- **OpenAI Integration:**  
  Utilizes GPT-4.1 Mini for fast, high-quality, and cost-effective tweet generation.
- **Automated Posting:**  
  Posts directly to Twitter using the v2 API, with support for scheduled/recurring tweets.
- **Dry-Run Mode:**  
  Can generate and preview tweets without posting (useful for testing or API limitations).
- **History & CLI:**  
  Command-line interface for posting, scheduling, and viewing tweet history.

### 🧠 How It Works

1. **User Context:**  
   Loads your profile, interests, and recent thoughts from a JSON file for deep personalization.
2. **Prompt Engineering:**  
   Dynamically builds system and user prompts tailored to your context and the selected content type.
3. **Content Generation:**  
   Calls OpenAI's GPT-4.1 Mini to generate tweet text, ensuring it fits your style and Twitter's character limit.
4. **Posting:**  
   Authenticates with Twitter using OAuth, then posts the generated tweet via the API.
5. **Scheduling (Optional):**  
   Can run on a schedule to post at regular intervals, keeping your feed active and relevant.

---

**Built for students, builders, and anyone who wants to share their journey authentically on Twitter, with zero manual effort.**

## Features

- 🤖 **AI-Powered Content**: Uses OpenAI GPT-4 to generate tweets
- 👤 **Personal Context**: Learns your style, interests, and current projects
- ⏰ **Automated Scheduling**: Posts at specified times throughout the day
- 📊 **Post History**: Tracks all posts with analytics
- 🧪 **Dry Run Mode**: Test content generation without posting
- 🔒 **Safe & Configurable**: Control topics, tone, and posting frequency

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

#### OpenAI API Key
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key for your `.env` file

#### Twitter API Keys
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or use existing one
3. Go to "Keys and tokens" tab
4. Generate all required keys:
   - Consumer Key & Secret
   - Bearer Token
   - Access Token & Secret

### 3. Configuration

1. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`**:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
   TWITTER_CONSUMER_KEY=your_twitter_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
   POSTING_SCHEDULE=09:00,14:00,19:00
   ```

3. **Update your profile in `user_context.json`**:
   ```json
   {
     "profile": {
       "name": "Your Name",
       "bio": "Your bio/description",
       "interests": ["AI", "Programming", "Startups"],
       "profession": "Software Developer",
       "location": "San Francisco",
       "writing_style": "casual, informative, occasionally humorous"
     },
     "current_projects": [
       {
         "name": "Twitter Bot",
         "description": "Building an AI-powered Twitter bot",
         "status": "in progress"
       }
     ],
     "recent_thoughts": [
       "The intersection of AI and social media is fascinating",
       "Building tools that reflect authentic personality"
     ],
     "posting_preferences": {
       "topics_to_avoid": ["politics", "controversial topics"],
       "preferred_hashtags": ["#AI", "#coding", "#tech"],
       "tone": "professional but friendly",
       "include_questions": true,
       "include_tips": true
     }
   }
   ```

## Usage

### Test Connections
```bash
python main.py test
```

### Generate and Post Manually
```bash
# Post with random context
python main.py post

# Post with specific context
python main.py post --context tip

# Generate without posting (dry run)
python main.py post --dry-run
```

### Start Automated Scheduler
```bash
python main.py schedule
```

### View Post History
```bash
python main.py history
python main.py history --limit 5
```

## Context Types

The bot can generate different types of content:

- **general**: General interesting thoughts or insights
- **project**: Updates about your current projects
- **thought**: Based on your recent thoughts/interests
- **tip**: Helpful tips related to your expertise
- **question**: Engaging questions for your followers

## File Structure

```
twitter-bot/
├── main.py              # CLI interface
├── bot.py               # Main bot class
├── content_generator.py # OpenAI content generation
├── twitter_client.py    # Twitter API client
├── scheduler.py         # Automated scheduling
├── config.py           # Configuration management
├── user_context.json   # Your profile and context
├── requirements.txt    # Dependencies
├── .env.example       # Environment variables template
├── bot.log            # Bot activity logs
├── post_history.json  # History of posted tweets
└── README.md          # This file
```

## Safety Features

- **Content Review**: All generated content respects your preferences
- **Character Limits**: Automatically ensures tweets fit Twitter's limits
- **Error Handling**: Robust error handling with detailed logging
- **Rate Limiting**: Respects Twitter's rate limits
- **Topic Filtering**: Avoids topics you specify as off-limits

## Customization

### Posting Schedule
Edit `POSTING_SCHEDULE` in your `.env` file:
```env
POSTING_SCHEDULE=09:00,13:00,17:00,21:00
```

### Writing Style
Update the `writing_style` and `tone` in `user_context.json` to match your preferred voice.

### Content Types
Modify the context types and prompts in `content_generator.py` to add new content categories.

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Double-check your API keys in `.env`
2. **Content Generation Fails**: Verify OpenAI API key and credits
3. **Posting Fails**: Ensure Twitter app has write permissions
4. **Scheduler Not Working**: Check posting times format (HH:MM)

### Logs
Check `bot.log` for detailed error messages and activity logs.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the bot!

## License

MIT License - feel free to use and modify as needed. 