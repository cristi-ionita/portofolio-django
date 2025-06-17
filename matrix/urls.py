from django.urls import path
from .views import home_view, projects_view, weather_view, speed_ping_view, loto_view

urlpatterns = [
    path('', home_view, name='home'),
    path('projects/', projects_view, name='projects'),
    path('weather/', weather_view, name='weather'),
    path('projects/speed-ping/', speed_ping_view, name='speed_ping'),
    path('loto/', loto_view, name='loto'),
]
