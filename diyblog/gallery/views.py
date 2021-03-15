from django.shortcuts import render
from .models import Gallery
from .serializers import GallerySerializer
from rest_framework import generics


class GalleryList(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
