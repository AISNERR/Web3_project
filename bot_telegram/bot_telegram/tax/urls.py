from django.urls import path
from . import views

urlpatterns = [
    path('telegram/', views.telegram),
]
