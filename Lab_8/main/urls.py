from django.urls import include, path
from rest_framework import routers
from .views import TeamViewSet, PlayerViewSet, create_team, update_team, delete_team

router = routers.DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('teams/create/', create_team),
    path('teams/update/<int:pk>/', update_team),
    path('teams/delete/<int:pk>/', delete_team),
]
