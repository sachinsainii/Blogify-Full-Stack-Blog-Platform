from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib import messages, admin
from taggit.models import Tag
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser 
import csv
#from django_filters.views import FilterView


def post_list(request):
    # post = get_object_or_404(Post)
    category_id = request.GET.get("category")
    tag_id = request.GET.get("tag")
    author_id = request.GET.get("author")
    # print("author_id",author_id)
    posts = Post.objects.filter(published_date__lte= timezone.now()).order_by('published_date')

    if category_id:
        posts = posts.filter(category_id=category_id)
    
    if tag_id:
        posts = posts.filter(tags__id=tag_id)

    if author_id:
        posts = posts.filter(author_id=author_id)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    User = get_user_model()
    users = User.objects.all()
    # print("users", list(users))


    return render(request, 'post_list.html',
     {'posts': posts, "categories": categories, "tags":tags, "users":users, })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # comments = post.comments.all().order_by('-created_date')
    comments  = post.comments.filter(parent__isnull=True)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                parent_id = request.POST.get('parent_id')
                parent_obj = None
                if parent_id:
                    try:
                       parent_obj = Comment.objects.get(id=parent_id)
                    except Comment.DoesNotExist:
                        parent_obj = None

                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.parent = parent_obj
                comment.save()
                return redirect('blog:post_detail',pk=pk)
        else:
            return redirect('api:user_login')
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments':comments, 'form':form })
    
@login_required
def post_new(request):

    # if Post.author != request.user:
    #     return HttpResponseForbidden("You are not allowed to create new post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            print(request.user)#new
            post.author = request.user
            post.published_date = timezone.now()
            print("Category selected:",post.category)
            # form.save()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

@login_required
def post_edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk,) #author=request.user)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            
            post.published_date = timezone.now()
            #form.save()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('blog:post_list')

    return render(request, 'post_delete.html',{'post':post})

# def post_tag(request, tag_slug):
#     tag = get_objects_or_404(Tag, slug=tag_slug)
#     posts = Post.objects.filter(tag=tag)
#     return render(request, 'post_detail.html',{'posts':posts,'tag':tag})

# def post_category(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     # posts = Post.objects.filter(category=category)
#     posts = category.posts.all().order_by('-published_date')
#     return render(request, 'post_category.html',{'category':category, 'posts':posts})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail',pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html',{'form':form, 'comment':comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this comment")

    if request.method == "POST":
        post_pk = comment.post.pk
        comment.delete()
        return redirect('blog:post_detail',pk=post_pk)

    return render(request, 'delete_comment.html',{'comment':comment})
    
def user_profile(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    return render(request, "user_profile.html",{"profile_user":user})

def about(request):
    return render(request, 'about.html')




