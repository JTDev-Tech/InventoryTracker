from django.http import HttpResponsePermanentRedirect, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.

def index(request: HttpRequest)->HttpResponsePermanentRedirect:
    return redirect('inventory:home', permanent=True)