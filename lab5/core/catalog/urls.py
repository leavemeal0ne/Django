from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('apartments/',views.apartments),
    path('additions/',views.additions),
    path('contacts/',views.contacts),
]