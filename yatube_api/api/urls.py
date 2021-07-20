from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter(trailing_slash='optional')
router_v1.register('posts/?', PostViewSet)
router_v1.register('groups/?', GroupViewSet)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments/?',
    CommentViewSet, basename="comments")

urlpatterns = [

    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
