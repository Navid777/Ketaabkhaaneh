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

def text_editor(request):
    return render(request, 'text_editor.html', {})

def text_editor_get_images(request, page):
    page = int(page)
    images = Image.objects.all().order_by('-date_added')[page*5:page*5+4];
    return render(request, 'image_page.json', {
        'images': images,
    })

def text_editor_get_videos(request, page):
    page = int(page)
    videos = Video.objects.all().order_by('-date_added')[page*5:page*5+4];
    return render(request, 'video_page.json', {
        'videos': videos,
    })
