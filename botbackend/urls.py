from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render
from django.shortcuts import HttpResponse
import asyncio
import webview 

def landing(request):
    return render(request,"landing.html")
  

def instruction(request):
    return render(request,"instruction.html")




urlpatterns = [
    path("admin/", admin.site.urls),
    path("support/",include("support.urls")),
    path("",include("bot.urls")),
    path("done/",landing),
    # path("publish/",publish),
    path("insturction/",instruction),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]


