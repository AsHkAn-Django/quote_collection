from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path('quote/quote_delete/<int:pk>/', views.QuoteDeleteView.as_view(), name='quote_delete'),
    path('quote/quote_edit/<int:pk>/', views.QuoteUpdateView.as_view(), name='quote_edit'),
    path('quote/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('quote/<int:pk>/comment/<int:comment_id>/add_subcomment/', views.add_subcomment, name='add_subcomment'),
    path('quote/quote_detail/<int:pk>/', views.quote_detail, name='quote_detail'),
    path('quote/quote_new/', views.QuoteCreateView.as_view(), name='quote_new'),
    path('quote/quote_list/', views.QuoteListView.as_view(), name='quote_list'),
    path('quote/quote_list/like/<int:pk>/', views.like, name='like'),
    path('', views.IndexView.as_view(), name='home'),
]

