# Telegram Entertainment Bot 🤖

A fun and educational Telegram bot project that delivers clean jokes and safe memes to users. This bot was developed as part of a college project to demonstrate proficiency in Python programming, API integration, and bot development.


## 🎯 Project Objectives

This project demonstrates:
- API integration and handling
- Error handling and logging
- Content filtering and safety measures
- User interface design with inline keyboards
- Bot deployment and management

## ✨ Features

- **Clean Jokes**: Fetches and filters jokes from JokeAPI to ensure appropriate content
- **Safe Memes**: Retrieves memes from Reddit via Meme API with NSFW filtering
- **Interactive Interface**: User-friendly inline keyboard buttons for easy navigation
- **Content Filtering**: Robust filtering system to block inappropriate content
- **Error Handling**: Comprehensive error handling for API failures and edge cases
- **Logging**: Detailed logging for debugging and monitoring
- **Multiple Commands**: Various commands for different functionalities

## 🛠️ Technical Implementation

### Architecture
- **Main Class**: `TelegramEntertainmentBot` - Core bot functionality
- **Async Programming**: Uses `asyncio` for non-blocking operations
- **API Integration**: Connects to external APIs for content retrieval
- **Content Safety**: Implements multiple layers of content filtering

### Key Components
1. **Command Handlers**: Handle user commands (`/start`, `/joke`, `/meme`, `/help`)
2. **Callback Query Handler**: Manages inline button interactions
3. **Content Filters**: Ensure all content is appropriate and safe
4. **Error Management**: Graceful error handling and user feedback

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Internet connection for API access

### Installation Steps

1. **Clone or download the project files**
   ```bash
   git clone [your-repository-url]
   cd telegram-entertainment-bot
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your bot token**
   
   **For Windows PowerShell:**
   ```powershell
   $env:BOT_TOKEN="your_bot_token_here"
   ```
   
   **For Linux/Mac:**
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

### Getting a Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the provided token
5. Set it as the `BOT_TOKEN` environment variable

## 📖 Usage Guide

### Available Commands
- `/start` - Initialize the bot and see welcome message
- `/joke` - Get a random clean joke
- `/meme` - Get a random safe meme
- `/help` - Display help information

### Interactive Features
- **Inline Buttons**: Quick access to jokes and memes
- **Loading Messages**: User feedback during content fetching
- **Error Messages**: Clear communication when issues occur

## 🔒 Content Safety Features

### Joke Filtering
The bot filters out jokes containing:
- NSFW content
- Religious content
- Political content
- Racist content
- Sexist content
- Explicit content

### Meme Filtering
The bot ensures memes are:
- Not marked as NSFW
- Not containing spoilers
- From appropriate subreddits
- Complete with required metadata

## 📊 Project Structure

```
telegram-entertainment-bot/
├── main.py              # Main bot implementation
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🔍 Code Highlights

### Asynchronous Programming
```python
async def fetch_clean_joke(self, max_attempts: int = 10) -> Optional[Dict[str, Any]]:
    # Demonstrates async/await pattern and error handling
```

### Content Filtering
```python
def is_joke_clean(self, joke_data: Dict[str, Any]) -> bool:
    # Implements comprehensive content safety checks
```

### API Integration
```python
response = requests.get(JOKE_API_URL, timeout=10)
response.raise_for_status()
```

## 🧪 Testing

The bot includes several testing scenarios:
- API failure handling
- Content filtering validation
- User interaction flows
- Error recovery mechanisms

## 📈 Learning Outcomes

Through this project, the following concepts were learned and implemented:
- **Python Programming**: Object-oriented design, async programming
- **API Integration**: REST API consumption, error handling
- **Bot Development**: Telegram Bot API, user interaction design
- **Content Management**: Filtering algorithms, safety measures
- **Software Engineering**: Code organization, documentation, logging

## 🚀 Future Enhancements

Potential improvements for future versions:
- Database integration for user preferences
- Custom joke categories
- User rating system for content
- Multi-language support
- Advanced content recommendation
- Admin panel for bot management

## 📝 Dependencies

- `python-telegram-bot==20.7` - Telegram Bot API wrapper
- `requests==2.31.0` - HTTP library for API calls
- `python-dotenv==1.0.0` - Environment variable management
- `asyncio` - Asynchronous programming support

## ⚠️ Important Notes

- This bot requires active internet connection
- API rate limits may affect response times
- Content filtering is based on API flags and may not be 100% perfect
- Bot token should be kept secure and not shared publicly

## 🎓 Academic Reflection

This project provided hands-on experience with:
- Real-world API integration challenges
- User experience design considerations
- Content moderation complexities
- Asynchronous programming benefits
- Error handling best practices



## 📜 License

This project is created for educational purposes as part of college coursework.

---

**Disclaimer**: This bot is a student project developed for educational purposes. All content is filtered for appropriateness, but users should use discretion when sharing with others.
