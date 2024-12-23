from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render
from django.shortcuts import HttpResponse
import asyncio

def landing(request):
   
   return render(request,'landing.html')

  
   
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("bot.urls")),
    path("done/",landing),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
