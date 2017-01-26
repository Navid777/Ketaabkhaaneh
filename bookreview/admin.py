from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from bookreview.models import *
import bs4

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    exclude = ('reference',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    exclude = ('reference',)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    exclude = ('reference',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(ArticleAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            url(r'^(?P<id>\d+)/edit/$',
                self.admin_site.admin_view(self.edit),
                name='%s_%s_edit' % info),
            url(r'^(?P<id>\d+)/edit/save/$',
                self.admin_site.admin_view(self.edit_save),
                name='%s_%s_edit_save' % info),
            url(r'^(?P<id>\d+)/edit/images/(?P<page>\d+)/$',
                self.admin_site.admin_view(self.edit_images),
                name='%s_%s_edit_images' % info),
            url(r'^(?P<id>\d+)/edit/videos/(?P<page>\d+)/$',
                self.admin_site.admin_view(self.edit_videos),
                name='%s_%s_edit_videos' % info),
        ] + urls

    @csrf_exempt
    def edit_save(self, request, id):
        obj = self.get_object(request, unquote(id))
        if request.method != "POST" or obj is None:
            raise Http404()
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        soup = bs4.BeautifulSoup(request.POST['source'], 'lxml')
        for img in soup.findAll('img'):
            if not img.has_attr('data-type'):
                continue

            template_tag = None
            if img['data-type'] == 'image':
                template_tag = 'render_image'
            elif img['data-type'] == 'video':
                template_tag = 'render_video'

            if not img.has_attr('data-id') or template_tag is None:
                img.decompose()
                continue

            tag = "{% " + template_tag + " id=" + img['data-id'] + " ";
            for attr in ['height', 'width', 'style']:
                if img.has_attr(attr):
                    tag += attr + "=\"" + img[attr] + "\" ";
                else:
                    tag += attr + "=None ";
            tag += "render_type=render_type %}"
            img.replace_with(tag)

        text = "{% load media_tags %}"
        if soup.body:
            text += soup.body.renderContents()
        elif soup.html:
            text += soup.html.renderContents()
        else:
            text += soup.renderContents()

        obj.text = text
        obj.save()
        return HttpResponse()

    def edit_images(self, request, id, page):
        page = int(page)
        images = Image.objects.all().order_by('-date_added')[page*5:page*5+4];
        return TemplateResponse(request, 'image_page.json', {
            'images': images,
        })

    def edit_videos(self, request, id, page):
        page = int(page)
        videos = Video.objects.all().order_by('-date_added')[page*5:page*5+4];
        return TemplateResponse(request, 'video_page.json', {
            'videos': videos,
        })

    def edit(self, request, id):
        model = self.model
        obj = self.get_object(request, unquote(id))
        if obj is None:
            raise Http404(
                _("%(name)s object with primary key %(key)r does not exist.") % {
                                'name': force_text(model._meta.verbose_name),
                                'key': escape(object_id),
                            })
        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        opts = model._meta
        app_label = opts.app_label
        context = dict(
            self.admin_site.each_context(request),
            title=_('Edit Rich Text: %s') % force_text(obj),
            module_name=capfirst(force_text(opts.verbose_name_plural)),
            object=obj,
            opts=opts,
            preserved_filters=self.get_preserved_filters(request),
        )
        request.current_app = self.admin_site.name

        return TemplateResponse(request, 'text_editor.html', context)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
