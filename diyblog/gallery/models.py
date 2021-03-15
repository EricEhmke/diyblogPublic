from django.db import models
from io import BytesIO
from django.core.files import File
from PIL import Image


class Gallery(models.Model):
    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='gallery', null=True, blank=True, height_field='height', width_field='width')
    description = models.TextField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    alt_text = models.TextField(blank=True, null=True, max_length=125)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.srcSet:
            image1024px = ResizedImage(image=resize_image(self.image, size=(1024, 1024)), original_image=self)
            image640px = ResizedImage(image=resize_image(self.image, size=(640, 640)), original_image=self)
            image320px = ResizedImage(image=resize_image(self.image, size=(320, 320)), original_image=self)
            image1024px.save()
            image640px.save()
            image320px.save()


class ResizedImage(models.Model):
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='gallery', height_field='height', width_field='width')
    original_image = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='srcSet')


def resize_image(image, size):
    """Resizes images to the given size"""

    im = Image.open(image)
    im.load()
    im.convert('RGB')
    im.thumbnail(size)
    thumb_io = BytesIO()
    im.save(thumb_io, 'JPEG', quality=90)
    resized_image = File(thumb_io, name=image.name)

    return resized_image
