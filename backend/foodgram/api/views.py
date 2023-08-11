from django.shortcuts import render
from rest_framework import decorators, filters, status, viewsets
from rest_framework.response import Response

from recipes.models import Favorite, Recipe, Ingredient, Tag
from api.serializers import RecipeSerializer, RecipeCreateSerializer, IngredientSerializer, TagSerializer
from users.serializers import RecipeSubscriptionSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return Recipe.objects.prefetch_related('recipe_ingredient__ingredient', 'tags').all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer
    
    @decorators.action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        if not Recipe.objects.filter(pk=pk).exists():
                return Response({'error': 'Нет рецепта с таким id'}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user, recipe=Recipe.objects.get(pk=pk)).exists():
                return Response({'error': 'Рецепт уже находится в избранном'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipeSubscriptionSerializer(Recipe.objects.get(pk=pk))
            Favorite.objects.create(user=request.user, recipe=Recipe.objects.get(pk=pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=request.user, recipe=Recipe.objects.get(pk=pk)).exists():
                return Response({'error': 'Данный рецепт не добавлен в избранное'}, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.filter(user=request.user, recipe=Recipe.objects.get(pk=pk)).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
