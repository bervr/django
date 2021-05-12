from django.urls import path, re_path
from authapp.views import authapp

app_name= 'authapp'

urlpatterns = [
   path('login/', authapp.login, name='login'),
   path('logout/', authapp.login, name='logout'),
]
