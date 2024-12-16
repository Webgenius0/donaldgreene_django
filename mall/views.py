from django.shortcuts import render
from django.shortcuts import get_object_or_404

# import from rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

# import from apps 
from .models import Product, Category, ColorVariant, SizeVariant, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer


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


class CartAPIView(APIView):
    def get(self, request):
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Cart get successful",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Product added to cart successfully",
            # "data": CartItemSerializer(cart_item).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request):
    
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        action = request.data.get('action')

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Item deleted from cart",
                    # "data": CartItemSerializer(cart_item).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
        cart_item.save()
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Cart updated successfully",
            # "data": CartItemSerializer(cart_item).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request):
    
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')

        if product_id:
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.delete()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Item deleted from cart",
                # "data": CartItemSerializer(cart_item).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            cart.items.all().delete()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Cart cleared",
            }
            return Response(response_data, status=status.HTTP_200_OK)