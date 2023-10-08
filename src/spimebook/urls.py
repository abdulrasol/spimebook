"""spimebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('writers/', include('writers.urls', namespace='writers')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('books/', include('books.urls', namespace='books')),
    # path('ratings/', include('star_ratings.urls', namespace='ratings')),
    # path('ajax/', include('reactions.urls', namespace='reactions')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

# urlpatterns += i18n_patterns(
# path('admin/', admin.site.urls),
# path('blog/', include('blog.urls')),
# path('authors/', include('authors.urls', namespace='authors')),
# )
