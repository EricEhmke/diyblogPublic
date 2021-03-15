from django.urls import path
from . import views

urlpatterns = [
    path('gallery/photos/', views.GalleryList.as_view()),
]
