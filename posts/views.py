from django.shortcuts import render
import telegram
import asyncio
from .models import Post
from django.http import JsonResponse
from telegram.error import BadRequest
from django.shortcuts import redirect


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_publish(request, pk):
    post = Post.objects.get(pk=pk)
    # Initialize bot with token
    bot = telegram.Bot(token="6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww")
    try:
        # Send message to channel
        channel_id = "-1001975486063"  # Channel ID for Selam Bingo announcements
        message_text = f"📢 New Announcement\n\n{post.title}\n\n{post.content}"
        
        # Use asyncio to handle the async bot call
        async def send_message():
            await bot.send_message(chat_id=channel_id, text=message_text)
            
        # Run the async function
        asyncio.run(send_message())
        
    except BadRequest as e:
        # Handle errors like bot not being admin in channel
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        # Handle other errors
        return JsonResponse({'error': 'Failed to publish post'}, status=500)

    return redirect('post_detail', pk=pk)

def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'posts/post_edit.html', {'post': post})

def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')

