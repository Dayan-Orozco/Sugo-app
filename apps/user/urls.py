from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home, name="dashboard_sugo"),    
    ### GESTIÓN DE USUARIOS ###
    path('streamers/', list_user, name='user_list'),
    path('streamers/<int:pk>/activate/', activate_user, name='user_activate'),    
    path('streamers/edit/<str:username>/', edit_user, name='user_edit'),
    # path('streamers/edit/', list_user, name='user_list'),
    # path('streamers/detail/', list_user, name='user_list'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name="register"),
    path('validate-reset-pin/', register, name="register"),
    path('reset-pin/', reset_pin, name="reset-password"),
]
