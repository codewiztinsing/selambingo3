import asyncio
from telegram import Bot
import telegram

bot = Bot(token='6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww')
async def main():
   
    try:
        chat = await bot.get_chat('tinsae')
        print(chat.id)
    except telegram.error.BadRequest as e:
        print(f"Error: {e}")


async def send_command(chat_id, command):

    res = await bot.send_message(chat_id=chat_id, text=f'/{command}')
    print("res = ",res)


if __name__ == "__main__":
    asyncio.run(send_command("1464395537","withdraw"))
