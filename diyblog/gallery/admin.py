from django.contrib import admin
from .models import Gallery
# Register your models here.


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('description', 'image', 'created_on', 'alt_text')
    fields = ['image', 'description', 'alt_text']


admin.site.register(Gallery, GalleryAdmin)
