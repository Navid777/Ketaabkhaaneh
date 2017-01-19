from django.shortcuts import render
from bookreview.models import *


def home(request):
    return render(request, 'home.html')


def article(request):
    return render(request, 'article.html')


def articles(request):
    return render(request, 'articles.html')


def text(request):
    return render(request, 'text.html')
