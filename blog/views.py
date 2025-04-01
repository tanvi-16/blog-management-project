from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from blog import models
from .models import Post, Userimage
from .models import SoftDelete
from django.utils import timezone
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.views import View
from datetime import datetime
from django.shortcuts import get_object_or_404  
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin



class Signup(View):
    def get(self, request):
         return render(request, 'blog/signup.html')
    
    def post(self, request):
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')
        #confirm_password = request.POST.get('uconfirmpassword')
    
        newUser = User.objects.create_user(username=name, email=email, password=password)
        newUser.save()
        return redirect('/')


class Login(View):
    def get(self, request):
        return render(request, 'blog/login.html')
    
    def post(self, request):
        name = request.POST.get('uname')
        password = request.POST.get('upassword')
        userr = authenticate(request, username=name, password=password)
        if userr is not None:
            login(request, userr)
            return redirect('/home')
        else:
            return redirect('/')


class Signout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class Home(View):
    def get(self, request):
        context = {
            'posts': Post.objects.all()
        }
        return render(request, 'blog/home.html', context)

 
class NewPost(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'blog/newpost.html')

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        npost = models.Post(title=title, content=content, category=category, author=request.user)
        npost.save()
        return redirect('/home')



class MyPost(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'posts': Post.objects.filter(author= request.user)
        }
        return render(request, 'blog/mypost.html', context)


def search(request):
    query=request.GET['search']
    allPosts= Post.objects.filter(category__icontains=query)
    params={'allPosts': allPosts}
    return render(request, 'blog/search.html', params)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']  

@login_required
def update(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=obj)
        if form.is_valid():
            obj.updated_time = datetime.now()  # Update the timestamp
            form.save()  # Save the updated post
            return redirect('/home')  # Redirect to the home page after saving
    else:
        form = PostForm(instance=obj)  # Populate the form with the existing post data

    return render(request, 'blog/update.html', {'form': form, 'post': obj})


@login_required
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.soft_delete()
        #post.delete()
        return redirect('/home')  
    return render(request, 'blog/delete.html', {'post': post})