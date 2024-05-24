"""merchex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bands/', views.band_list, name='band-list'),
    path('bands/<int:id>/', views.band_detail, name='band-detail'),
    path('bands/add/', views.band_create, name='band-create'),
    path('bands/<int:id>/change/', views.band_update, name='band-update'),
    path('bands/<int:id>/delete/', views.band_delete, name='band-delete'),
    path('about-us/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
    path('email-sent/', views.email_sent, name='email-sent'),
    path('ads/', views.ad_list, name='ad-list'),
    path('ads/<int:id>/', views.ad_detail, name='ad-detail'),
    path('ads/add/', views.ad_create, name='ad-create'),
    path('ads/<int:id>/change/', views.ad_update, name='ad-update'),
    path('ads/<int:id>/delete', views.ad_delete, name='ad-delete'),
    
]
