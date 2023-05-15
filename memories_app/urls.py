from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings
from .views import base_views, user_views, story_views
from django.views.generic import TemplateView


# We don't need to have views for the pages where we can just use templates.
# Sign up page for example doesn't have a data to be retrieved so we can just add
# it's template as view in urls.py. These are CLASS BASED VIEWS.
# The rest is FUNCTION BASED VIEWS that we need to define in views.py

urlpatterns = [
    # path('users/create', user_views.create_user),
    path('',base_views.base_view, name='base'),
    path('login', TemplateView.as_view(template_name='memories/login.html'), name='login'),
    # path('users/', user_views.get_all_users, name='users'),
    path('signup/', TemplateView.as_view(template_name='memories/signup.html'), name='signup'),
    path('create_user/', user_views.create_user, name='create_user'),
    path('login_user/', user_views.login_user, name='login_user'),
    path('logout_user/', user_views.logout_user, name='logout_user'),
    path('lost_password/', TemplateView.as_view(template_name='memories/lost_password.html'), name='lost_password'),
    path('lost_password/reset_password/', user_views.reset_password, name='reset_password'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/update_profile', user_views.update_profile, name='update_profile'),
    path('create_post/', story_views.create_post, name='create_post'),
    path('search_post/', story_views.search_post, name='search_post'),
    path('landing_page/', story_views.landing_page, name='landing_page'),
    path('story/<int:story_id>/', story_views.story_detail, name='story_detail'),
    path('like_story/',story_views.like_story, name='like_story'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)