from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('products/<int:pk>/', views.ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('users/', views.UserAPIView.as_view()),
]
