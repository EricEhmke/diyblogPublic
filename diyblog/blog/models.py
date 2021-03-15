from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
import uuid


STATUS = (
    (0, "DRAFT"),
    (1, "Publish")
)


class Tag(models.Model):
    # Fields
    name = models.CharField(max_length=20, help_text='Enter a post subject')

    # Functions
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tags', args=[str(self.id)])


class ImageUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this picture')
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to="gallery")
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, help_text="Upload images for this post", null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('image', args=[str(self.id)])


class LeadImage(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='gallery', null=True, blank=True)
    alt_text = models.CharField(max_length=200, null=True, blank=True)


class BlogPost(models.Model):
    # Fields
    leadimage = models.ForeignKey("LeadImage", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=1000)
    firstpublished = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    author = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    text = RichTextUploadingField(config_name='default')
    tags = models.ManyToManyField(Tag, help_text='Tag this post with keywords')
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField()

    # Functions
    def display_tags(self):
        return ', '.join(tag.name for tag in self.tag.all())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-firstpublished']

    def get_absolute_url(self):
        return reverse('posts-detail', kwargs={'slug': self.slug, 'id': self.id})


class Comment(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this comment')
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    author = models.TextField(max_length=25, default='Anonymous')
    text = models.TextField()
    published = models.DateField(auto_now_add=True)
    approvedcomment = models.BooleanField(default=False)

    # Meta
    class Meta:
        ordering = ['published']

    def approve(self):
        self.approvedcomment = True
        self.save()

