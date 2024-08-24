from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', BlogHome.as_view(), name='home'),
    path('category/<slug:category_slug>/', PostsCategory.as_view(), name='category'),  # Изменено на slug
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),  # This is the like_post URL
    path('add/', AddPostView.as_view(), name='add_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

