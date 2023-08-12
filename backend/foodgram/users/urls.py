from django.urls import include, path
from rest_framework import routers
from users.views import CustomUserViewSet, SubscriptionViewSet, set_password

router = routers.SimpleRouter()
router.register('', CustomUserViewSet)

urlpatterns = [
    path(
        'subscriptions/',
        SubscriptionViewSet.as_view({'get': 'list'}),
        name='subscriptions',
    ),
    path('set_password/', set_password, name='set_password'),
    path('', include(router.urls)),
]
