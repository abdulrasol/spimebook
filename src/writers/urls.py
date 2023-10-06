from django.urls import path
from writers.views import writers , writer, add
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'writers'
urlpatterns = [
    path('', writers, name='writers'),
    path('<int:pk>/', writer, name='writer'),
    path('add/',add, name='add-writer'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
