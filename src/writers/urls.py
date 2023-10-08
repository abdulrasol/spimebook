from django.urls import path
from writers.views import Writers, add, search_writer, WriterDetail
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'writers'
urlpatterns = [
    path('', Writers.as_view(), name='writers'),
    path('<int:pk>/', WriterDetail.as_view(), name='writer'),
    path('add/', add, name='add-writer'),
    path('find/<str:name>/', search_writer, name='find-writer'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
