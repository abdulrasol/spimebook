from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test', views.test, name='test'),
    path('quotes/', views.quotes, name='quotes'),
    path('posts/<str:user>', views.my_posts, name='my-posts'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit-post'),
    path('post/new', views.new_post, name='new-post'),
    path('comment/<int:post_id>/', views.add_comment, name='add-comment'),
    #path('love/<int:post_id>', views.love, name='love'),
    path('save/<int:post_id>', views.save, name='save'),
    # ajax
    path('ajax/post/love/<int:post_id>', views.love, name='love'),
]
