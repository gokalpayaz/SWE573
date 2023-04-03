from django.urls import path
from .views import user_views
from django.views.generic import TemplateView


# We don't need to have views for the pages where we can just use templates.
# Sign up page for example doesn't have a data to be retrieved so we can just add
# it's template as view in urls.py. These are CLASS BASED VIEWS.
# The rest is FUNCTION BASED VIEWS that we need to define in views.py

urlpatterns = [
    # path('users/create', user_views.create_user),
    path('users/', user_views.get_all_users, name='users'),
    path('signup/', TemplateView.as_view(template_name='memories/signup.html'), name='signup'),
    path('memories/create_user/', user_views.create_user, name='create_user')
]