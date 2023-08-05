from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from recipes.views import *

router = routers.SimpleRouter()
router.register('recipes', RecipeViewset)
router.register('tags', TagViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc',
    ),
]
