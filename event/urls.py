from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CommentViewSet
from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]