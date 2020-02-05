from django.urls import path
from account.views import (
    registeration_view,
    profile_view,
    logout_view,
    login_view,
    track_order,
            )

urlpatterns = [
    path('register/', registeration_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('track-order/',track_order, name='track')   
]