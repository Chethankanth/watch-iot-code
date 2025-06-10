from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'guardians', views.GuardianViewSet)
router.register(r'alerts', views.AlertViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('health-data/', views.process_health_data, name='process-health-data'),
    path('chat/', views.chat_with_health_assistant, name='chat-with-health-assistant'),
]