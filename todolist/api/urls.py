from api.views import ParseAstanaHubView, TaskViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'parse-astanahub/',
        ParseAstanaHubView.as_view(),
        name='parse-astanahub'
    ),
]
