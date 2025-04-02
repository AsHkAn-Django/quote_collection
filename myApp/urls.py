from django.urls import path
from . import views

urlpatterns = [
    path('quote/quote_delete/<int:pk>/', views.QuoteDeleteView.as_view(), name='quote_delete'),
    path('quote/quote_edit/<int:pk>/', views.QuoteUpdateView.as_view(), name='quote_edit'),
    path('quote/quote_detail/<int:pk>/', views.QuoteDetailView.as_view(), name='quote_detail'),
    path('quote/quote_new/', views.QuoteCreateView.as_view(), name='quote_new'),
    path('quote/quote_list/', views.QuoteListView.as_view(), name='quote_list'),
    path('note/like/<int:pk>', views.like, name='like'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.IndexView.as_view(), name='home'),
]

