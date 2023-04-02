from django.urls import path
from .views import user_views

urlpatterns = [
    # path('users/create', user_views.create_user),
    path('users', user_views.get_all_users),
]