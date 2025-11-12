"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from apps.sugo import views

urlpatterns = [
    path('dashboard/', views.home, name="dashboard_sugo"),
    # Streamers
    path('streamer/register/', views.register_streamer, name="streamer_register"),    
    path('streamers/', views.list_streamer, name='streamer_list'),
    path('streamers/<int:pk>/edit/', views.edit_streamer, name='streamer_edit'),
    path('streamers/<int:pk>/delete/', views.delete_streamer, name='streamer_delete'),
    path('streamers/upload-excel/', views.upload_excel, name='streamer_upload_excel'),
    path('streamers/<int:pk>/capacitar/', views.capacitar_streamer, name='streamer_capacite'),
    path('streamers/<int:pk>/set-join-date/', views.set_join_date, name='streamer_set_join_date'),
    # Registro Diario 
    path('daily/', views.list_daily_performance, name='daily_list'),
    path('daily/upload-excel/', views.upload_excel_daily_performance, name='daily_upload_excel'),


]
