from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render
from django.shortcuts import HttpResponse
import asyncio
import webview 

def landing(request):
    try:
        asyncio.run(webview.notify_telegram_user("Payment method setup completed successfully"))
    except Exception as e:
        print(f"Error notifying user: {e}")
    return HttpResponse("done")

#    try:
#        webview.destroy_window()
#    except:
#        pass
#    return HttpResponse("done")

  
   
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("bot.urls")),
    path("done/",landing),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
