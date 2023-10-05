from django.urls import path
from writers.views import writers , writer, add

app_name = 'writers'
urlpatterns = [
    path('', writers, name='writers'),
    path('<int:pk>/', writer, name='writer'),
    path('add/',add, name='add-writer'),
]
