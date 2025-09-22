import logging
import os
import requests
from typing import Optional, Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes,
    MessageHandler,
    filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# API URLs
JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any"
MEME_API_URL = "https://meme-api.com/gimme"

class TelegramEntertainmentBot:
    
    def __init__(self, token: str):

        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("joke", self.joke_command))
        self.application.add_handler(CommandHandler("meme", self.meme_command))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        welcome_message = (
            "🎉 Welcome to the Entertainment Bot! 🎉\n\n"
            "I'm here to brighten your day with clean jokes and memes!\n\n"
            "Available commands:\n"
            "• /joke - Get a random clean joke\n"
            "• /meme - Get a random safe meme\n"
            "• /help - Show this help message\n\n"
            "All content is filtered to be appropriate! 📚✨"
        )
        
        # Create inline keyboard for quick actions
        keyboard = [
            [
                InlineKeyboardButton("😂 Get Joke", callback_data="get_joke"),
                InlineKeyboardButton("🤣 Get Meme", callback_data="get_meme")
            ],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        help_message = (
            "🤖 Entertainment Bot Help\n\n"
            "Commands:\n"
            "• /start - Start the bot and see welcome message\n"
            "• /joke - Get a random clean joke\n"
            "• /meme - Get a random safe meme\n"
            "• /help - Show this help message\n\n"
            "Content Filtering:\n"
            "• All jokes are filtered for NSFW, religious, political, racist, sexist, and explicit content\n"
            "• All memes are checked for NSFW and spoiler content\n"
            "• Only appropriate content is delivered\n\n"
            "Enjoy responsibly! 📚🎉"
        )
        await update.message.reply_text(help_message)
    
    async def joke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /joke command."""
        await update.message.reply_text("🔍 Searching for a clean joke... Please wait!")
        await asyncio.sleep(2)
        joke_data = await self.fetch_clean_joke()
        
        if joke_data:
            await self.send_joke(update, joke_data)
        else:
            await update.message.reply_text(
                "😅 Sorry, I couldn't find a clean joke right now. "
                "Please try again in a moment!"
            )
    
    async def meme_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /meme command."""
        await update.message.reply_text("🔍 Searching for a safe meme... Please wait!")
        # to simulate loading and prevent hitting API too quickly
        await asyncio.sleep(2)

        meme_data = await self.fetch_safe_meme()
        
        if meme_data:
            await self.send_meme(update, meme_data)
        else:
            await update.message.reply_text(
                "😅 Sorry, I couldn't find a safe meme right now. "
                "Please try again in a moment!"
            )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks."""
        query = update.callback_query
        await query.answer()
        
        # Check if current message has text or is a photo
        is_photo_message = bool(query.message.photo)
        
        if query.data == "get_joke":
            if is_photo_message:
                # If current message is a photo, send a new loading message
                loading_msg = await query.message.reply_text("🔍 Searching for a clean joke... Please wait!")
                # Delete the old meme message
                await query.message.delete()
            else:
                # If current message is text, edit it
                await query.edit_message_text("🔍 Searching for a clean joke... Please wait!")
                loading_msg = None
            
            joke_data = await self.fetch_clean_joke()
            if joke_data:
                if loading_msg:
                    await self.send_joke_new_message(loading_msg, joke_data)
                else:
                    await self.send_joke_callback(query, joke_data)
            else:
                error_message = ("😅 Sorry, I couldn't find a clean joke right now. "
                               "Please try again in a moment!")
                if loading_msg:
                    await loading_msg.edit_text(error_message)
                else:
                    await query.edit_message_text(error_message)
        
        elif query.data == "get_meme":
            if is_photo_message:
                # If current message is a photo, send a new loading message
                loading_msg = await query.message.reply_text("🔍 Searching for a safe meme... Please wait!")
                # Delete the old meme message
                await query.message.delete()
            else:
                # If current message is text, edit it
                await query.edit_message_text("🔍 Searching for a safe meme... Please wait!")
                loading_msg = None
            
            meme_data = await self.fetch_safe_meme()
            if meme_data:
                if loading_msg:
                    await self.send_meme_new_message(loading_msg, meme_data)
                else:
                    await self.send_meme_callback(query, meme_data)
            else:
                error_message = ("😅 Sorry, I couldn't find a safe meme right now. "
                               "Please try again in a moment!")
                if loading_msg:
                    await loading_msg.edit_text(error_message)
                else:
                    await query.edit_message_text(error_message)
        
        elif query.data == "help":
            help_message = (
                "🤖 Entertainment Bot Help\n\n"
                "Commands:\n"
                "• /start - Start the bot\n"
                "• /joke - Get a clean joke\n"
                "• /meme - Get a safe meme\n"
                "• /help - Show help\n\n"
                "All content is appropriate! 📚✨"
            )
            if is_photo_message:
                # If current message is a photo, delete it and send new text
                await query.message.delete()
                await query.message.reply_text(help_message)
            else:
                await query.edit_message_text(help_message)
    
    async def fetch_clean_joke(self, max_attempts: int = 10) -> Optional[Dict[str, Any]]:
        """
        Fetch a clean joke from the JokeAPI.
        
        Args:
            max_attempts: Maximum number of API calls to find a clean joke
            
        Returns:
            Dictionary containing joke data if found, None otherwise
        """
        for attempt in range(max_attempts):
            try:
                response = requests.get(JOKE_API_URL, timeout=10)
                response.raise_for_status()
                
                joke_data = response.json()
                # Check if the joke is clean (all flags should be False for appropriate content)
                if self.is_joke_clean(joke_data):
                    logger.info(f"Found clean joke after {attempt + 1} attempts")
                    return joke_data
                else:
                    logger.info(f"Joke filtered out (attempt {attempt + 1}): inappropriate content")
                    continue
                    
            except requests.RequestException as e:
                logger.error(f"Error fetching joke (attempt {attempt + 1}): {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error fetching joke (attempt {attempt + 1}): {e}")
                continue
        
        logger.warning(f"Failed to find clean joke after {max_attempts} attempts")
        return None
    
    async def fetch_safe_meme(self, max_attempts: int = 10) -> Optional[Dict[str, Any]]:
        """
        Fetch a safe meme from the Meme API.
        
        Args:
            max_attempts: Maximum number of API calls to find a safe meme
            
        Returns:
            Dictionary containing meme data if found, None otherwise
        """
        for attempt in range(max_attempts):
            try:
                response = requests.get(MEME_API_URL, timeout=10)
                response.raise_for_status()
                
                meme_data = response.json()
                
                # Check if the meme is safe (not NSFW and not spoiler)
                if self.is_meme_safe(meme_data):
                    logger.info(f"Found safe meme after {attempt + 1} attempts")
                    return meme_data
                else:
                    logger.info(f"Meme filtered out (attempt {attempt + 1}): inappropriate content")
                    continue
                    
            except requests.RequestException as e:
                logger.error(f"Error fetching meme (attempt {attempt + 1}): {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error fetching meme (attempt {attempt + 1}): {e}")
                continue
        
        logger.warning(f"Failed to find safe meme after {max_attempts} attempts")
        return None
    
    def is_joke_clean(self, joke_data: Dict[str, Any]) -> bool:
        """
        Check if a joke is appropriate.
        
        Args:
            joke_data: Dictionary containing joke data from API
            
        Returns:
            True if joke is clean, False otherwise
        """
        if not isinstance(joke_data, dict):
            return False
        
        # Check for error in API response
        if joke_data.get("error", True):
            return False
        
        # Get flags - all should be False for clean content
        flags = joke_data.get("flags", {})
        
        # List of flags that make content inappropriate
        inappropriate_flags = [
            "nsfw", "religious", "political", "racist", "sexist", "explicit"
        ]
        
        # Check if any inappropriate flag is True
        for flag in inappropriate_flags:
            if flags.get(flag, True):  # Default to True (unsafe) if flag is missing
                return False
        
        # Additional check: the joke should be marked as safe
        if not joke_data.get("safe", False):
            return False
        
        return True
    
    def is_meme_safe(self, meme_data: Dict[str, Any]) -> bool:
        """
        Check if a meme is appropriate.
        
        Args:
            meme_data: Dictionary containing meme data from API
            
        Returns:
            True if meme is safe, False otherwise
        """
        if not isinstance(meme_data, dict):
            return False
        
        # Check if meme is NSFW or spoiler
        if meme_data.get("nsfw", True):  # Default to True (unsafe) if missing
            return False
        
        if meme_data.get("spoiler", True):  # Default to True (unsafe) if missing
            return False
        
        # Check if required fields are present
        required_fields = ["title", "url", "author"]
        for field in required_fields:
            if field not in meme_data:
                return False
        
        return True
    
    async def send_joke_new_message(self, loading_msg, joke_data: Dict[str, Any]):
        """Send a joke by editing the loading message."""
        try:
            if joke_data["type"] == "single":
                joke_text = f"😂 **Random Joke**\n\n{joke_data['joke']}"
            else:  # two-part joke
                joke_text = (
                    f"😂 **Random Joke**\n\n"
                    f"**Setup:** {joke_data['setup']}\n\n"
                    f"**Punchline:** {joke_data['delivery']}"
                )
            
            # Add category and ID for reference
            joke_text += f"\n\n📁 Category: {joke_data.get('category', 'Unknown')}"
            joke_text += f"\n🔢 ID: {joke_data.get('id', 'Unknown')}"
            
            # Create inline keyboard for more actions
            keyboard = [
                [
                    InlineKeyboardButton("😂 Another Joke", callback_data="get_joke"),
                    InlineKeyboardButton("🤣 Get Meme", callback_data="get_meme")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await loading_msg.edit_text(joke_text, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error sending joke new message: {e}")
            await loading_msg.edit_text("Sorry, there was an error sending the joke. Please try again!")
    
    async def send_meme_new_message(self, loading_msg, meme_data: Dict[str, Any]):
        """Send a meme by deleting the loading message and sending a photo."""
        try:
            # Format caption with title in bold and author info
            caption = (
                f"**{meme_data['title']}**\n\n"
                f"👤 Author: {meme_data['author']}\n"
                f"📱 Subreddit: r/{meme_data['subreddit']}\n"
                f"🔗 [Original Post]({meme_data['postLink']})"
            )
            
            # Create inline keyboard for more actions
            keyboard = [
                [
                    InlineKeyboardButton("🤣 Another Meme", callback_data="get_meme"),
                    InlineKeyboardButton("😂 Get Joke", callback_data="get_joke")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Delete the loading message and send photo
            await loading_msg.delete()
            await loading_msg.reply_photo(
                photo=meme_data['url'],
                caption=caption,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error sending meme new message: {e}")
            await loading_msg.edit_text("Sorry, there was an error sending the meme. Please try again!")

    async def send_joke(self, update: Update, joke_data: Dict[str, Any]):
        """Send a joke as a text message."""
        try:
            if joke_data["type"] == "single":
                joke_text = f"😂 **Random Joke**\n\n{joke_data['joke']}"
            else:  # two-part joke
                joke_text = (
                    f"😂 **Random Joke**\n\n"
                    f"**Setup:** {joke_data['setup']}\n\n"
                    f"**Punchline:** {joke_data['delivery']}"
                )
            
            # Add category and ID for reference
            joke_text += f"\n\n📁 Category: {joke_data.get('category', 'Unknown')}"
            joke_text += f"\n🔢 ID: {joke_data.get('id', 'Unknown')}"
            
            # Create inline keyboard for more actions
            keyboard = [
                [
                    InlineKeyboardButton("😂 Another Joke", callback_data="get_joke"),
                    InlineKeyboardButton("🤣 Get Meme", callback_data="get_meme")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(joke_text, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error sending joke: {e}")
            await update.message.reply_text("Sorry, there was an error sending the joke. Please try again!")
    
    async def send_joke_callback(self, query, joke_data: Dict[str, Any]):
        """Send a joke as response to callback query."""
        try:
            if joke_data["type"] == "single":
                joke_text = f"😂 **Random Joke**\n\n{joke_data['joke']}"
            else:  # two-part joke
                joke_text = (
                    f"😂 **Random Joke**\n\n"
                    f"**Setup:** {joke_data['setup']}\n\n"
                    f"**Punchline:** {joke_data['delivery']}"
                )
            
            # Add category and ID for reference
            joke_text += f"\n\n📁 Category: {joke_data.get('category', 'Unknown')}"
            joke_text += f"\n🔢 ID: {joke_data.get('id', 'Unknown')}"
            
            # Create inline keyboard for more actions
            keyboard = [
                [
                    InlineKeyboardButton("😂 Another Joke", callback_data="get_joke"),
                    InlineKeyboardButton("🤣 Get Meme", callback_data="get_meme")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(joke_text, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error sending joke callback: {e}")
            await query.edit_message_text("Sorry, there was an error sending the joke. Please try again!")
    
    async def send_meme(self, update: Update, meme_data: Dict[str, Any]):
        """Send a meme as a photo with caption."""
        try:
            # Format caption with title in bold and author info
            caption = (
                f"**{meme_data['title']}**\n\n"
                f"👤 Author: {meme_data['author']}\n"
                f"📱 Subreddit: r/{meme_data['subreddit']}\n"
                f"🔗 [Original Post]({meme_data['postLink']})"
            )
            
            # Create inline keyboard for more actions
            keyboard = [
                [
                    InlineKeyboardButton("🤣 Another Meme", callback_data="get_meme"),
                    InlineKeyboardButton("😂 Get Joke", callback_data="get_joke")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send photo with caption
            await update.message.reply_photo(
                photo=meme_data['url'],
                caption=caption,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error sending meme: {e}")
            await update.message.reply_text("Sorry, there was an error sending the meme. Please try again!")
    
    async def send_meme_callback(self, query, meme_data: Dict[str, Any]):
        """Send a meme as response to callback query."""
        try:
            # Format caption with title in bold and author info
            caption = (
                f"**{meme_data['title']}**\n\n"
                f"👤 Author: {meme_data['author']}\n"
                f"📱 Subreddit: r/{meme_data['subreddit']}\n"
                f"🔗 [Original Post]({meme_data['postLink']})"
            )
            
            # Create inline keyboard for more actions
            keyboard = [
                [
                    InlineKeyboardButton("🤣 Another Meme", callback_data="get_meme"),
                    InlineKeyboardButton("😂 Get Joke", callback_data="get_joke")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Delete the previous message and send new photo
            await query.message.delete()
            await query.message.reply_photo(
                photo=meme_data['url'],
                caption=caption,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error sending meme callback: {e}")
            await query.edit_message_text("Sorry, there was an error sending the meme. Please try again!")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors that occur during bot operation."""
        logger.error(f"Update {update} caused error {context.error}")
        
        # Notify user of error if possible
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "🔧 Sorry, something went wrong! Please try again later."
            )
    
    def run(self):
        """Start the bot."""
        logger.info("Starting Entertainment Bot...")
        print("🤖 Entertainment Bot is starting...")
        print("📚 All content is filtered for appropriate material!")
        print("🔄 Press Ctrl+C to stop the bot")
        
        try:
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            print(f"\n❌ Error running bot: {e}")

def main():
    """Main function to start the bot."""
    # Get bot token from environment variable or prompt user
    bot_token = os.getenv("BOT_TOKEN")
    
    if not bot_token:
        print("🔑 Bot token not found in environment variables.")
        print("Please set the BOT_TOKEN environment variable with your Telegram bot token.")
        print("\nTo get a bot token:")
        print("1. Message @BotFather on Telegram")
        print("2. Send /newbot command")
        print("3. Follow the instructions to create your bot")
        print("4. Copy the token and set it as BOT_TOKEN environment variable")
        print("\nExample (Windows PowerShell):")
        print('$env:BOT_TOKEN="your_bot_token_here"')
        print("\nExample (Linux/Mac):")
        print('export BOT_TOKEN="your_bot_token_here"')
        return
    
    # Create and run the bot
    bot = TelegramEntertainmentBot(bot_token)
    bot.run()

if __name__ == "__main__":
    main()