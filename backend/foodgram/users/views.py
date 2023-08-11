from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

from users.models import CustomUser, Subscription
from users.serializers import CustomUserSerializer, CustomUserCreateSerializer, SubscriptionSerializer

class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer
    
    @decorators.action(detail=True, methods=['post', 'delete'], serializer_class=SubscriptionSerializer)
    def subscribe(self, request, id):
        if request.method == 'POST':
            if Subscription.objects.filter(author=CustomUser.objects.get(pk=id), subscriber=request.user).exists():
                return Response({"error": "Вы уже подписаны на данного автора"}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.get(pk=id)==request.user:
                return Response({"error": "Нельзя подписываться на себя"}, status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(author=CustomUser.objects.get(pk=id), subscriber=request.user)
            serializer = self.get_serializer_class()(CustomUser.objects.get(pk=id), data=request.data)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not Subscription.objects.filter(author=CustomUser.objects.get(pk=id), subscriber=request.user).exists():
            return Response({"error": "Вы итак не подписаны на данного автора"}, status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.delete(author=CustomUser.objects.get(pk=id), subscriber=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(subscribers__subscriber=self.request.user)
