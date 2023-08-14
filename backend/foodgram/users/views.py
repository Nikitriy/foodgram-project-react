from django.contrib.auth.tokens import default_token_generator
from djoser.views import UserViewSet
from rest_framework import decorators, status, viewsets
from rest_framework.response import Response
from users.models import CustomUser, Subscription
from users.serializers import (CustomUserCreateSerializer,
                               CustomUserSerializer, SetPasswordSerializer,
                               SubscriptionSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @decorators.action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id):
        if request.method == 'POST':
            if Subscription.objects.filter(
                author=CustomUser.objects.get(id=id), subscriber=request.user
            ).exists():
                return Response(
                    {"error": "Вы уже подписаны на данного автора"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if CustomUser.objects.get(id=id) == request.user:
                return Response(
                    {"error": "Нельзя подписываться на себя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = SubscriptionSerializer(CustomUser.objects.get(id=id))
            Subscription.objects.create(
                author=CustomUser.objects.get(id=id), subscriber=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Subscription.objects.filter(
                author=CustomUser.objects.get(id=id), subscriber=request.user
            ).exists():
                return Response(
                    {"error": "Вы итак не подписаны на данного автора"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Subscription.objects.filter(
                author=CustomUser.objects.get(id=id), subscriber=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(
            subscribers__subscriber=self.request.user
        )


@decorators.api_view(['POST'])
def set_password(request):
    if request.method == 'POST':
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.user.password)
        if request.user.password != serializer.data.get('current_password'):
            return Response(
                {'error': 'Неверно введён существующий пароль'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        CustomUser.objects.filter(username=request.user.username).update(
            password=serializer.data.get('new_password')
        )
        return Response(
            {'message': 'Пароль успешно изменён'},
            status=status.HTTP_204_NO_CONTENT,
        )
