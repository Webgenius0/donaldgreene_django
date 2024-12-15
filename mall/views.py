from django.shortcuts import render

# import from rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

# import from apps 
from .models import Product, Category, ColorVariant, SizeVariant
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer 
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    def perform_create(self, serializer): 
        serializer.save(user=self.request.user) 
