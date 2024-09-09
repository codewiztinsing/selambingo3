from django.shortcuts import render

# Create your views here.


def pay_with_chapa(request):
    context = {}
    return render(request,"payments/index.html",context)