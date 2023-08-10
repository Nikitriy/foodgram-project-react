from django.urls import include, path
from rest_framework import routers

from users.views import *


router = routers.SimpleRouter()
router.register('', CustomUserViewSet)

urlpatterns = [
    path('subscriptions/', SubscriptionViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('', include(router.urls)),
]

