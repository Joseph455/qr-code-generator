from django.urls import path
from QrWebApp.views import home, post_url

urlpatterns = [
    path('', home, name='home'),
    path('post/', post_url, name='post'),
]
