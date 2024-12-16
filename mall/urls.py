from django.urls import path
from . import views

urlpatterns = [
    path('products/list/',views.ProductListView.as_view()),
    path('product/', views.ProductListCreateView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view()),


    path('cart/', views.CartAPIView.as_view(), name='cart'),


]

