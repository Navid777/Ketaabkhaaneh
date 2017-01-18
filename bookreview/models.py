from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import os


class Reference(models.Model):
    PERSON = 1
    BOOK = 2
    FILM = 3
    type = models.IntegerField(choices=(
        (PERSON, "Person"),
        (BOOK, "Book"),
        (FILM, "Film"),
    ))
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        if self.type == self.PERSON:
            return "Person: " + unicode(self.person)
        if self.type == self.BOOK:
            return "Book: " + unicode(self.book)
        if self.type == self.FILM:
            return "Film: " + unicode(self.film)
        return "Error!"


class Person(models.Model):
    name = models.CharField(max_length=256)
    original_name = models.CharField(max_length=256, null=True, blank=True)
    #TODO: remove default when admin is fixed
    reference = models.OneToOneField(Reference, related_name="person", blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.reference = Reference.objects.create(type=Reference.PERSON)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    original_title = models.CharField(max_length=256, null=True, blank=True)
    author = models.ForeignKey(Person, related_name='books')
    translator = models.ForeignKey(Person, null=True, blank=True,
                                   related_name='books_translated')
    #TODO: remove default when admin is fixed
    reference = models.OneToOneField(Reference, related_name='book', blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.reference = Reference.objects.create(type=Reference.BOOK)
        super(Book, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Film(models.Model):
    title = models.CharField(max_length=256)
    original_title = models.CharField(max_length=256, null=True, blank=True)
    director = models.ForeignKey(Person, related_name='films')
    writer = models.ForeignKey(Person, null=True, blank=True,
                               related_name='films_written')
    actors = models.ManyToManyField(Person, related_name='films_acted')
    #TODO: remove when admin is fixed
    reference = models.OneToOneField(Reference, related_name='film', blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.reference = Reference.objects.create(type=Reference.FILM)
        super(Film, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=256)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=256)
    alt_text = models.TextField()
    image = models.FileField(upload_to=settings.IMAGE_UPLOAD_TO)
    thumbnail = models.FileField(upload_to=settings.IMAGE_UPLOAD_TO, blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def generate_thumbnail(self):
        print "1"
        if not self.image:
            return

        print "2"
        if self.thumbnail:
            return

        print "3"
        from PIL import Image
        from cStringIO import StringIO

        THUMBNAIL_SIZE = (100,100)

        if (self.image.name.endswith(".jpg") or
            self.image.name.endswith(".JPG") or
            self.image.name.endswith(".jpeg")):
            image_type = 'image/jpeg'
            pil_type = 'jpeg'
            ext = 'jpg'
        elif (self.image.name.endswith(".png") or
              self.image.name.endswith(".PNG")):
            image_type = 'image/png'
            pil_type = 'png'
            ext = 'png'
        else:
            print "WTF: " + self.image.name
            return

        image = Image.open(StringIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        handle = StringIO()
        image.save(handle, pil_type)
        handle.seek(0)

        thumb_file = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                            handle.read(),
                                            content_type=image_type)
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(thumb_file.name)[0], ext),
            thumb_file,
        )

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

        self.generate_thumbnail()

    def __unicode__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=256)
    video = models.FileField(upload_to=settings.VIDEO_UPLOAD_TO)
    thumbnail = models.FileField(upload_to=settings.VIDEO_UPLOAD_TO, blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def generate_thumbnail(self):
        if not self.video:
            return

        if self.thumbnail:
            return

        from moviepy.editor import *
        import tempfile

        clip = VideoFileClip(self.video.path)

        step = (clip.duration - 0.1) / 19

        for i in xrange(18, 0, -1):
            clip = clip.cutout(0.1+i*step, step+i*step)
        clip = clip.resize((100, 100))

        temp = tempfile.NamedTemporaryFile(suffix='.gif')
        clip.write_gif(temp.name, fps=12)

        thumb_file = SimpleUploadedFile(os.path.split(self.video.name)[-1],
                                        temp.read(),
                                        content_type='image/gif')
        temp.close()
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(thumb_file.name)[0], 'gif'),
            thumb_file,
        )

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)

        self.generate_thumbnail()

    def __unicode__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=1024)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='articles')
    reference = models.ForeignKey(Reference, related_name='articles')
    adl_references = models.ForeignKey(Reference, related_name='adl_articles')
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=128)
    text = models.TextField()
    article = models.ForeignKey(Article, related_name='comments')
    date_added = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        if len(self.text) > 30:
            return self.name + ": " + self.text[:27] + "..."
        return self.name + ": " + self.text


admin.site.register(Reference)
admin.site.register(Person)
admin.site.register(Book)
admin.site.register(Film)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Article)
admin.site.register(Comment)
