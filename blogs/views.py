from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db.models import Q

# Create your views here.


def index(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    posts = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(author__username__icontains=q))
    return render(request, 'index.html', {'posts': posts})


def login(request):
    return render(request, 'loginPage.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.info(request, 'Email or Username already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
    else:
        return render(request, 'registerPage.html')
    

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'loginPage.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('index')

@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        post = Post(author=request.user, title=title, body=content)
        post.save()
        return redirect('index')
    else:
        return render(request, 'create-post.html')
    
def post(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'post.html', {'post': post})


def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return redirect('index')
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        post.title = title
        post.body = content
        post.save()
        return redirect('index')
    else:
        return render(request, 'edit-post.html', {'post': post})