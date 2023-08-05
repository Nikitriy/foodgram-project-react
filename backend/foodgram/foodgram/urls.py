from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from recipes.views import *

router = routers.SimpleRouter()
router.register('recipes', RecipeViewset)
router.register('tags', TagViewset)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api", include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc',
    ),
]
