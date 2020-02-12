from django.views import generic
from .models import Category, Post, Comment
from django import forms
from .forms import CommentForm
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django import http


class PostList(generic.ListView):
    template_name = 'index.html'
    def get(self, request):
        posts = Post.objects.filter(status=1).order_by('-created_on')
        categories = Category.objects.all().order_by('title')
        args = {'posts': posts, 'categories': categories}
        return render(request, self.template_name, args)

def category_detail(request, slug):
    template_name = 'category_detail.html'
    categories = Category.objects.all().order_by('title')
    category_detail = Category.objects.filter(slug=slug)
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    args = {'posts' : posts, 'categories': categories}
    return render(request, template_name, args)

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)



def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.filter(status=1).order_by('-created_on')
    categories = Category.objects.all().order_by('title')
    comments = post.comments.filter(active=True)
    new_comment = None
    form = CommentForm(request.POST)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)
        else:
            form = CommentForm()
   # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
           # Assign the current post to the comment
            new_comment.post = post
           # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'posts':posts,
                                           'categories':categories,
                                           'comments': comments,
                                           'form': form,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':post,
    }
    return render(request, 'index.html', context)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)