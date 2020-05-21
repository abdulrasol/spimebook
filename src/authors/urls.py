from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('', views.authors, name='authors'),
    path('add/', views.add_author, name='add-author'),
    path('<int:author_id>/<str:author_name>', views.author, name='author'),
    path('<int:author_id>/<str:author_name>/edit',
         views.edit_author, name='edit-author'),

    # AJAX
    path('ajax/author_autocomplete/',
         views.author_autocomplete, name='author-autocomplete'),

]
