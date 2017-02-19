from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

def index_view(request):
    return render(request, 'view1.html', {
        'some_var': 'This is value of some_var'
    })
