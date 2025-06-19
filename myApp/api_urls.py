from rest_framework.routers import DefaultRouter
from . import api_views
from django.urls import path, include

app_name = 'myApp'

router = DefaultRouter()
router.register(r'quotes', api_views.QuoteViewSet, basename='quotes')

urlpatterns = [
    path('', include(router.urls)),
]


