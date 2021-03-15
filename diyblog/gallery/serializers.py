from rest_framework import serializers
from .models import Gallery, ResizedImage


class ResizedImageField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.image.url} {value.width}w"


class GallerySerializer(serializers.ModelSerializer):
    src = serializers.ImageField(source='image')
    alt = serializers.CharField(source='alt_text')
    srcSet = ResizedImageField(many=True, queryset=ResizedImage.objects.all())
    sizes = serializers.ReadOnlyField(default=["(max-width: 600px) 100vw,(min-width: 500px) 50vw,100vw"])

    class Meta:
        model = Gallery
        fields = ('src', 'description', 'created_on', 'width', 'height', 'srcSet', 'sizes', 'alt')
