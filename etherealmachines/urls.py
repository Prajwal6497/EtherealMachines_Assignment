from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet

# Create a router and register the MachineViewSet with it
router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machine')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
