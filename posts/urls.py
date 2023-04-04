from django.urls import path 

from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='list'),
    path('posts/detail/<int:pk>', views.PostsDetailView.as_view(), name='detail'),
]