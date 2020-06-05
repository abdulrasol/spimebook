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
    path('user/recover/password', views.revover_password, name='recover-pass'),
    path('<str:username>/', views.user_profile, name='user-profile'),

    # ajax
    path('api/user/password-recover-get',
         views.send_token_pass, name='recover-pass-send-token'),
    path('api/user/password-recover-check',
         views.check_token_pass, name='recover-pass-check-token'),
    path('api/user/password-recover-reset',
         views.set_new_pass, name='recover-pass-set-new'),
]
