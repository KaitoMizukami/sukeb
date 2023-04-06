from django.urls import path

from . import views


app_name = 'authentications'

urlpatterns = [ 
    path('signup/', views.AuthenticationsSignupView.as_view(), name='signup'),
]