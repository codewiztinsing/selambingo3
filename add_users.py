import time
import asyncio
from telethon import TelegramClient, functions

# # Replace with your own values
# api_id = '22585626'
# api_hash = '265e49e697302c862bab5d08e767a76c'
# phone_number = '+251991221912'

api_id = '23715073'
api_hash = '32720265aaa34db0c33a377e06b2b60d'
phone_number = '+251925025885'


from telethon import TelegramClient

from telethon.tl.functions.channels import InviteToChannelRequest


# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

async def add_users_to_channel():
    channel_username = 'Selambingo'
    
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

    try:
        # Get the channel entity first
        channel = await client.get_entity(channel_username)
        print(f"Found channel {channel_username}")
        
        # Join the channel using the correct method
        await client(InviteToChannelRequest(channel, [username]))
       
        print(f"Successfully joined {channel_username}")
        
        # Add each unique user
        for username in unique_usernames:
            try:
                await client.add_chat_members(channel_username, username)
                print(f"Successfully added {username} to {channel_username}")
                # Add delay to avoid rate limits
                time.sleep(2)
                
            except Exception as e:
                print(f"Failed to add {username}: {str(e)}")
                
    except Exception as e:
        print(f"Failed to join channel {channel_username}: {str(e)}")

# Run the client
with client:
    client.loop.run_until_complete(add_users_to_channel())


