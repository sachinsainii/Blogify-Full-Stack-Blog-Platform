from django.db import models
from django.utils import timezone
from django.conf import settings
# from .models import Category
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/',blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='featured/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/',null=True,blank=True)
    # tags = models.ManyToManyField("Tag", blank=True, related_name="posts")

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)

    def __str__(self): 
        return f'Comment by {self.user.username} on "{self.post.title}"'




