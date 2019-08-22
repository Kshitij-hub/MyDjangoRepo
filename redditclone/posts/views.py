from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models
from .models import Post
from django.utils import timezone

# Create your views here.
@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['url']:
            post=models.Post();
            post.title=request.POST['title']
            post.url=request.POST['url']
            post.pub_date=timezone.datetime.now()
            post.author=request.user
            post.save()
            posts=Post.objects.order_by('-votes')
            return redirect('home')
        else:
            return render(request,"posts/create.html",{'error':"Error:Must contain TITLE and URL"})
    else:
        return render(request,"posts/create.html")



def home(request):
    posts=Post.objects.order_by('-votes')
    return render(request,"posts/home.html",{'posts':posts})

def upvote(request,id):
    if request.method == "POST":
        posts=Post.objects.get(pk=id)
        posts.votes += 1
        posts.save()
        return redirect('home')

def downvote(request,id):
    if request.method == "POST":
        posts=Post.objects.get(pk=id)
        posts.votes -= 1
        posts.save()
        return redirect('home')

def userposts(request,id):
    posts=Post.objects.filter(author_id=id).order_by('-votes')
    author=User.objects.get(pk=id)
    return render(request,"posts/userposts.html",{'posts':posts,'author':author})
