from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def publish(request):
    return render(request, 'publish.html')

def publish_blog(request):
    return render(request, 'publish_blog.html')


def publish_blog_post(request):
    return render(request, 'publish_blog_post.html')

def publish_blog_category(request):
    return render(request, 'publish_blog_category.html')

def publish_blog_image(request):
    return render(request, 'publish_blog_image.html')


def publish_blog_post(request):
    return render(request, 'publish_blog_post.html')

def publish_blog_category(request):
    return render(request, 'publish_blog_category.html')

def publish_blog_image(request):
    return render(request, 'publish_blog_image.html')

