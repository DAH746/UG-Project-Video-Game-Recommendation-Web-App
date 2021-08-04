from django.urls import path

from . import views

app_name = 'theSite'
urlpatterns = [
    path('', views.index, name='index'),
    path('searchForASpecificGame', views.specificGameSearch, name="specificGameSearch"),
    path('test', views.test, name='test'),
    path('ajax/inputtedGame', views.userInputtedGame, name='game_input_ajax')
]