from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    name = models.TextField()
    email = models.EmailField()
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    title = models.TextField()
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True)


class PublishHouse(models.Model):
    title = models.TextField()
    address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Article(models.Model):
    text = models.TextField()
    title = models.TextField()
    author = models.ForeignKey(Person, related_name='written_articles')
    translator = models.ForeignKey(Person, null=True, blank=True, related_name='translated_articles')
    thumbnail1 = models.ImageField(upload_to='article/thumbnails')
    thumbnail2 = models.ImageField(null=True, blank=True, upload_to='article/thumbnails')
    thumbnail3 = models.ImageField(null=True, blank=True, upload_to='article/thumbnails')
    main_image = models.ImageField(upload_to='article/images')
    categories = models.ManyToManyField(Category, related_name='articles')

    def thumbnails(self):
        thumbnails = [self.thumbnail1, self.thumbnail2, self.thumbnail3]
        return [x for x in thumbnails if x is not None]

    def __unicode__(self):
        return self.title


class Book(models.Model):
    title = models.TextField()
    edition = models.TextField()
    publisher = models.ForeignKey(PublishHouse, related_name='books')
    authors = models.ManyToManyField(Person, related_name='written_books')
    translators = models.ManyToManyField(Person, related_name='translated_books')
    isbn = models.CharField(max_length=20, null=True, blank=True)
    cover_image = models.ImageField()
    publish_date = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='books')
    articles = models.ManyToManyField(Article, related_name='books')

    def __unicode__(self):
        return self.title


class Movie(models.Model):
    title = models.TextField()
    directors = models.ManyToManyField(Person, related_name='directed_movies')
    actors = models.ManyToManyField(Person, related_name='played_movies')
    publish_date = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='movies')
    articles = models.ManyToManyField(Article, related_name='movies')

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article)
    parent = models.ForeignKey('self', null=True, blank=True)
    text = models.CharField(max_length=10000)
    email = models.EmailField(null=True, blank=True)
