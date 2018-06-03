from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'commits', views.CommitViewSet)
router.register(r'repositories', views.RepositoryViewSet)
