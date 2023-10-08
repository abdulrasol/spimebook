from django.urls import path
from profiles.views import UserProfile
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'profiles'
urlpatterns = [
    path('<int:pk>/', UserProfile.as_view(), name='profile')
]
urlpatterns = format_suffix_patterns(urlpatterns)
