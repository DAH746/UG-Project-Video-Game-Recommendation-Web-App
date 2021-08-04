from django.urls import path

from . import views

app_name = 'googleURL'
urlpatterns = [
    path('', views.google, name='google'),
]