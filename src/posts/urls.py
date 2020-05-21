from django.urls import path
from . import views
app_name = 'posts'
urlpatterns = [
    path('', views.home, name='posts'),
    path('test', views.test, name='test'),
    path('quotes/', views.quotes, name='quotes'),
    path('posts/<str:user>', views.my_posts, name='my-posts'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit-post'),
    path('save/<int:post_id>', views.save, name='save'),

]
