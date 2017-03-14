from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

def index_view(request):
    return render(request, 'index.html')
