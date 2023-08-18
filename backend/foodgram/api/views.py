from django.db.models import Sum
from django.http import HttpResponse
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

    def recipe_exists(self, pk):
        recipe = Recipe.objects.filter(pk=pk).first()
        if not recipe:
            return Response(
                {"error": "Рецепта с таким id не существует"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return recipe

    def post_method(self, request, model, validation, recipe):
        if validation:
            return Response(
                {"error": "Рецепт уже находится в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RecipeSubscriptionSerializer(recipe)
        model.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_method(self, request, model, validation, recipe):
        if not validation:
            return Response(
                {"error": "Данный рецепт не добавлен в избранное"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk):
        recipe = self.recipe_exists(pk)
        validation = recipe.favorite_users.user == request.user
        if request.method == "POST":
            return self.post_method(request, Favorite, validation, recipe)
        if request.method == "DELETE":
            return self.delete_method(request, Favorite, validation, recipe)

    @decorators.action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk):
        recipe = self.recipe_exists(pk)
        validation = recipe.shopping_cart_users.user == request.user
        if request.method == "POST":
            return self.post_method(request, ShoppingCart, validation, recipe)
        if request.method == "DELETE":
            return self.delete_method(
                request, ShoppingCart, validation, recipe
            )


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
