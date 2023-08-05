from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework import routers

from api.views import *

router = routers.SimpleRouter()
router.register('recipes', RecipeViewset)
router.register('tags', TagViewset)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]