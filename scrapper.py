import time
import asyncio
from telethon import TelegramClient



# Replace with your own values
# api_id = '22585626'
# api_hash = '265e49e697302c862bab5d08e767a76c'
# phone_number = '+251991221912'

api_id = '26670679'
api_hash = 'eb4656941f60304a79b2a81a89b40752'
phone_number = '+251911934565'




client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Read usernames from file
    with open('usernames.txt', 'r') as file:
        usernames = file.read().splitlines()
    
    # Remove duplicates while preserving order
    unique_usernames = []
    seen = set()
    for username in usernames:
        if username not in seen:
            unique_usernames.append(username)
            seen.add(username)

    # Message to send
    message = """
                🎯 20% Deposit Bonus 🎯
                    • Players receive a generous 20% bonus on all deposits! 💰
                    • Boost your playing power instantly! 🚀
                ✨ Advanced Features ✨
                    • User-Friendly Interface 📱
                    • Advanced Game Options 🎮 
                    • Full Mobile Compatibility 📲
                    • Active Community Chat Rooms 💬
                    • Exclusive Loyalty Rewards 👑
                🌟 Benefits of Using Selam Bingo 🌟
                    • Enhanced Gaming Experience with Bonuses 🎁
                    • Wide Variety of Exciting Games 🎲
                    • Vibrant Player Community 👥
                    • 24/7 Customer Support 🛟
                    • Secure & Fast Transactions 🔒
                Join us today and experience the best in online bingo! 🎉
                @SelamBingo_bot
                """
  
    # Send message to each unique username
    for username in unique_usernames:
      
        try:
           
            await client.send_message(username, message)
            print(f"Message sent to {username}")
        except Exception as e:
            print(f"Failed to send message to {username}: {str(e)}")
        
        # Add a small delay to avoid hitting rate limits
        time.sleep(6)

    


with client:
    client.loop.run_until_complete(main())
