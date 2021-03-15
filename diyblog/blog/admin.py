from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Comment, BlogPost, Tag, ImageUpload, LeadImage

# Register your models here.
admin.site.register(Comment)
# admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(ImageUpload)
admin.site.register(LeadImage)


class ImageUploadInline(admin.TabularInline):
    model = ImageUpload


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'firstpublished', 'status', 'firstpublished', 'author')
    list_filter = ("status",)

    fields = ['title', 'slug','leadimage', 'subtitle', 'author', 'text', 'status', 'tags']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(BlogPost, BlogPostAdmin)
