from django.urls import path
from QrWebApp.views import home, post_url

urlpatterns = [
    path('home/', home, name='home'),
    path('home/post/', post_url, name='post'),
]
