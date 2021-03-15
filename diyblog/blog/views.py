from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.syndication.views import Feed


# Create your views here.

from .models import Tag, BlogPost, Comment


def get_redirected(queryset_or_class, lookups, validators):
    """
    Calls get_object_or_404 and conditionally builds redirect URL
    """
    obj = get_object_or_404(queryset_or_class, **lookups)
    for key, value in validators.items():
        if value != getattr(obj, key):
            return obj, obj.get_absolute_url()
    return obj, None


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_posts = BlogPost.objects.all().count()
    num_comments = Comment.objects.all().count()
    posts = BlogPost.objects.filter(status=1)

    context = {
        'num_posts': num_posts,
        'num_comments': num_comments,
        'posts': posts,
    }

    return render(request, 'index.html', context=context)


class BlogPostListView(generic.ListView):
    """View function for detailed post view"""
    queryset = BlogPost.objects.filter(status=1).order_by('firstpublished')
    model = BlogPost


class BlogPostDetailView(generic.DetailView):
    model = BlogPost

    def my_view(self, request, slug, id):
        article, article_url = get_redirected(BlogPost, {'pk': id}, {'slug': slug})
        if article_url:
            return redirect(article_url)


class TagDetailView(generic.DetailView):
    """View function for detailed tag view"""
    model = Tag


def about(request):
    """View function for about page"""
    return render(request, 'about.html')


class BlogFeed(Feed):
    title = "Eric Ehmke - RSS Feed"
    link = ""
    description = "Latest posts from the blog of Eric Ehmke"

    def items(self):
        return BlogPost.objects.filter(status=1).order_by('firstpublished')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.subtitle
