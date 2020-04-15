from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<str:user>', views.my_post, name='my-posts'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('comment/<int:post_id>/', views.add_comment, name='add-comment'),
    #path('love/<int:post_id>', views.love, name='love'),
    path('save/<int:post_id>', views.save, name='save'),
    # ajax
    path('ajax/post/love/<int:post_id>', views.love, name='love'),
]
