from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import decorators, filters, status, viewsets
from rest_framework.response import Response

from api.permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.serializers import RecipeSubscriptionSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrIsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            "recipe_ingredient__ingredient", "tags"
        ).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH", "DELETE"):
            return RecipeCreateSerializer
        return RecipeSerializer

    def recipe_exists(self):
        if not Recipe.objects.first().exists():
            return Response(
                {"error": "Список рецептов пуст"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post_method(self, request, model, validation, pk):
        self.recipe_exists()
        if validation:
            return Response(
                {"error": "Рецепт уже находится в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RecipeSubscriptionSerializer(
            get_object_or_404(Recipe, pk=pk)
        )
        model.objects.create(
            user=request.user, recipe=get_object_or_404(Recipe, pk=pk)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_method(self, request, model, validation, pk):
        self.recipe_exists()
        if not validation:
            return Response(
                {"error": "Данный рецепт не добавлен в избранное"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.filter(
            user=request.user, recipe=get_object_or_404(Recipe, pk=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk):
        validation = (
            get_object_or_404(Recipe, pk=pk).favorite_users.user
            == request.user
        )
        if request.method == "POST":
            return self.post_method(request, Favorite, validation, pk)
        if request.method == "DELETE":
            return self.delete_method(request, Favorite, validation, pk)

    @decorators.action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk):
        validation = (
            get_object_or_404(Recipe, pk=pk).shopping_cart_users.user
            == request.user
        )
        if request.method == "POST":
            return self.post_method(request, ShoppingCart, validation, pk)
        if request.method == "DELETE":
            return self.delete_method(request, ShoppingCart, validation, pk)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@decorators.api_view(["GET"])
def shopping_cart(request):
    ingredients = (
        RecipeIngredient.objects.filter(
            recipe__shopping_cart_users__user=request.user
        )
        .values("ingredient__name", "ingredient__measurement_unit")
        .annotate(amount=Sum("amount"))
    )
    shopping_list = ""
    for ingredient in ingredients:
        shopping_list += (
            f'{ingredient["ingredient__name"]}'
            f'- {ingredient["amount"]}'
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    response = HttpResponse(shopping_list, content_type="text/plain")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={request.user.username}_shopping_list.txt"
    return response
