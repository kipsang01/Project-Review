from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('newpost',views.post_image,name='newpost'),
    path('post/<post_id>',views.post,name='post'),
    path('myprofile/edit', views.edit_profile, name='edit_my_profile'),
    path('myprofile/', views.my_profile, name='my_profile'),
    path('profile/<username>', views.user_profile, name='profile'),
    path('search/', views.search_post, name='search_post'),
    path('Api/posts/', views.PostsList.as_view(), name='PostApi'),
    path('Api/profiles/', views.UserProfiles.as_view(), name='PostApi'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
