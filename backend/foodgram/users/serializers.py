from rest_framework import serializers

from api.serializers import RecipeSubscriptionSerializer
from users.models import CustomUser, Subscription


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.ReadOnlyField(source='subscribers__is_subscribed', default=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.ReadOnlyField(default=False, source='subscribers__is_subscribed')
    recipes = RecipeSubscriptionSerializer(many=True, source='all_recipes')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')
    
    def get_recipes_count(self, obj):
        return obj.all_recipes.count()
