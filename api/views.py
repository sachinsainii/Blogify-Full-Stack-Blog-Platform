from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.http import JsonResponse
from .models import CustomUser,Postt
from blog.models import Post
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, user)
            # messages.success(request,"Account created successfully")
            return redirect('api:login')
            messages.success(request,"Account created successfully")

        else:
            print(form.errors)
            messages.error(request, "please correct the error")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html',{'form':form})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password= password)
        if user is not None:
            login(request, user)#new
            return redirect('blog:post_list')
            
        else:
            messages.error(request,"Invalid Email or password")
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    # return redirect('home')
    # print(request.user)
    return redirect('blog:post_list')
    

@login_required
def profile_view(request):
    user = request.user
    user.refresh_from_db()
    context = {'user_profile': user}
    return render(request, 'profile.html', context)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user) 
            return redirect('api:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile_edit.html',{'form':form})
 
@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    return render(request, 'my_posts.html',{'posts':posts})


    

