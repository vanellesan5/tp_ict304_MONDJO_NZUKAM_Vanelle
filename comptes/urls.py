from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompteViewSet

router = DefaultRouter()
router.register(r'comptes', CompteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]