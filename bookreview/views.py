from django.shortcuts import render, get_object_or_404
from bookreview.models import *


def home(request):
    return render(request, 'home.html')


def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article.html', {
        'article': article,
    })


def articles(request):
    return render(request, 'articles.html')


def text(request):
    return render(request, 'text.html')
