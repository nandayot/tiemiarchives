from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
# Create your models here.

#class Category(models.Model):
#    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
#    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated at")
#    title = models.CharField(max_length=255, verbose_name="Title")
#
#    class Meta:
#        verbose_name = "Category"
#        verbose_name_plural = "Categories"
#        ordering = ['title']
#
#    def __str__(self):
#        return self.title
class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-title']
    
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, verbose_name="Category")
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

def approved_comments(self):
    return self.comments.filter(approved_comment=True)