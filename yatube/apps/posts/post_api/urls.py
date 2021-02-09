from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, \
    SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (CommentViewSet, FollowViewSet, GroupViewSet, LikeViewSet,
                    PostViewSet)

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('group', GroupViewSet)
router.register('follow', FollowViewSet, basename='Follow')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='Comments')
router.register(r'posts/(?P<post_id>\d+)/likes', LikeViewSet, basename='Likes')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/', include(router.urls)),
    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/doc/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('v1/alterdoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
]
