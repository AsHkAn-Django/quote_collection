from . import views
from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign-up', views.UserCreateView.as_view(), name='signup'),
]