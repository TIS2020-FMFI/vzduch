"""vzduch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from pathlib import Path
from django.urls import path
from airMonitor.views.HomeView import HomeView
from airMonitor.views.VzduchView import VzduchView

urlpatterns = [
    path('graf', HomeView.as_view()),
    path('', HomeView.as_view()),
    path('vzduch', VzduchView.as_view()),
]
