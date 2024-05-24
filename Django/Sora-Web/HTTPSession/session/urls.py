from django.urls import path
from . import views

urlpatterns = [
    path('session/', views.create_session, name='create_session'),
    path('session/<uuid:session_uuid>/', views.confirm_session, name='confirm_session'),
]
