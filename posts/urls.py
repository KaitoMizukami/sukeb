from django.urls import path 

from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='list'),
    path('posts/detail/<int:pk>', views.PostsDetailView.as_view(), name='detail'),
    path('posts/create/', views.PostsCreateView.as_view(), name='create'),
    path('posts/delete/<int:pk>', views.PostsDeleteView.as_view(), name='delete'),
]