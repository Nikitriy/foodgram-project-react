from django.urls import include, path
from rest_framework import routers

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet
import users.urls

router = routers.SimpleRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('users/', include(users.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]