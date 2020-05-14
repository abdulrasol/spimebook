from django.urls import path
from . import views
app_name = 'reactions'
urlpatterns = [
    path('post/love/<int:post_id>', views.love, name='love'),
    path('post/comment/<int:post_id>', views.add_commnet, name='add-comment'),
    path('post/new/<int:book_id>', views.new_post, name='add-post'),
]
