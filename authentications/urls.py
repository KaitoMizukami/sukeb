from django.urls import path

from . import views


app_name = 'authentications'

urlpatterns = [ 
    path('signup/', views.AuthenticationsSignupView.as_view(), name='signup'),
    path('login/', views.AuthenticationsLoginView.as_view(), name='login'),
    path('logout/', views.AuthenticationsLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
]