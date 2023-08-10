from django.urls import include, path
from rest_framework import routers

from api.views import *
import users.urls

router = routers.SimpleRouter()
router.register('recipes', RecipeViewset)
router.register('tags', TagViewset)
router.register('ingredients', IngredientViewset)


urlpatterns = [
    path('users/', include(users.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]