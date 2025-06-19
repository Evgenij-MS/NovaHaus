from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # URL pattern for editing the current user's profile
    # This must come before the username pattern to avoid 'edit' being treated as a username
    path('edit/', views.profile_edit, name='profile_edit'),

    # URL pattern for viewing a user's profile
    path('<str:username>/', views.profile_detail, name='profile_detail'),
]
