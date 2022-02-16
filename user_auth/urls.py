import django
import django.contrib.auth.views
from django.urls import path,include
from . import views

app_name='user_auth'

urlpatterns=[
     path('',views.top_page, name = "default"),
     path('', views.top, name='index'),
     path('top/',views.top_page, name="top"), # リダイレクト
     path('login/', # ログイン
     django.contrib.auth.views.LoginView.as_view(template_name = 'user_auth/login.html'),
     name='login'),
     path('logout/', # ログアウト
     django.contrib.auth.views.LogoutView.as_view(template_name = 'user_auth/logout.html'),
     name='logout'),
]