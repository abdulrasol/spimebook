from django.urls import path
from . import views
from spimebook import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/login', views.log_in, name='log-in'),
    path('user/logout', views.log_out, name='log-out'),
    path('user/register', views.register, name='register'),
    path('user/profile', views.profile, name='profile'),
    path('user/profile/edit', views.edit_profile, name='edit-profile'),
    path('user/profile/settings', views.settings, name='settings'),
    path('<str:username>/', views.user_profile, name='user-profile'),
    path('local', views.local),

    # ajax
    #path('ajax/post/love/<int:post_id>', views.love, name='love'),
]
