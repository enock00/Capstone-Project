from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CommentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]