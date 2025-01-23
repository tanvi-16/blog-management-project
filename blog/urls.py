
from django.urls import path
from . import views
from blog.views import Signup, Login, Signout, Home, NewPost, MyPost
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('signup/', Signup.as_view(),  name='signup'),
    path('', Login.as_view(), name='login'),
    path('home/', Home.as_view(), name='home'),
    path('newpost/', NewPost.as_view(), name='newpost'),
    path('mypost/', MyPost.as_view(), name='mypost'),
    path('signout/', Signout.as_view(), name='signout'),
    path('search/', views.search, name="search"),
    path('update/<int:post_id>/', views.update, name="update"),
    path('mypost/update/<int:post_id>/', views.update, name="update"),
    path('mypost/delete/<int:post_id>/', views.delete, name="delete"),
    path('mypost/delete/', views.delete, name="delete")
]
