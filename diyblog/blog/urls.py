from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('posts/', views.BlogPostListView.as_view(), name='posts'),
	path('<slug:slug>,<int:id>/', views.BlogPostDetailView.as_view(), name='posts-detail'),
	path('tags/<str:pk>', views.TagDetailView.as_view(), name='tags'),
	path('about/', views.about, name='about'),
	path('rss/', views.BlogFeed(), name='rss'),
	path('summernote/', include('django_summernote.urls')),
	path('ckeditor/', include('ckeditor_uploader.urls')),
]
