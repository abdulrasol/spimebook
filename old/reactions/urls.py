from django.urls import path
from . import views
app_name = 'reactions'
urlpatterns = [
    path('post/love/<int:post_id>', views.love, name='love'),
    path('post/comment/<int:post_id>', views.add_commnet, name='add-comment'),
    path('post/new/<int:book_id>', views.new_post, name='add-post'),
    path('book/get_all_books', views.get_all_books, name='all-books'),
    path('mail/test', views.send_email, name='mail-test'),
]
