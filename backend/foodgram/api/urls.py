import users.urls
from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       shopping_cart)

router = routers.SimpleRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('recipes/download_shopping_cart/', shopping_cart),
    path('users/', include(users.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
