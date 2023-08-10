from django.shortcuts import render
from rest_framework import filters, viewsets

from recipes.models import *
from api.serializers import *

class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return Recipe.objects.prefetch_related('recipe_ingredient__ingredient', 'tags').all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
    
    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer


class IngredientViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class TagViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
