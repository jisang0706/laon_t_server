from django.shortcuts import render
from django.http import HttpResponse

def intro(request):
    return HttpResponse("Intro")