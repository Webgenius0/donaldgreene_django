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
from .models import Product, Category, ColorVariant, SizeVariant, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from business.models import BusinessProfile

# class ProductListView(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [AllowAny]
#     queryset = Product.objects.all() 
#     serializer_class = ProductSerializer


# class ProductListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ProductSerializer 
#     def get_queryset(self):
#         return Product.objects.filter(user=self.request.user)
#     def perform_create(self, serializer): 
#         serializer.save(user=self.request.user) 

class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, business_id,product_id=None, *args, **kwargs):
        try:
            business_profile = BusinessProfile.objects.get(id=business_id)
        except BusinessProfile.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Business profile not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        products = Product.objects.filter(business_profile=business_profile)
        if product_id:
            product = get_object_or_404(products, id=product_id)
            serializer = ProductSerializer(product)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Product fetch successful",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        serializer = ProductSerializer(products, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "message": "Products fetched successful",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request, business_id, *args, **kwargs):
        try:
            business_profile = BusinessProfile.objects.get(id=business_id)
        except BusinessProfile.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Business profile not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        data = request.data 
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(business_profile=business_profile, user=self.request.user)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Product created successful",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
    def put(self, request,business_id,product_id, *args,**kwargs):
        business_profile = BusinessProfile.objects.get(id=business_id)
        product = Product.objects.get(id=product_id, business_profile=business_profile)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Product updated successful",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
    def delete(self, request, business_id, product_id, *args,**kwargs):
        business_profile = BusinessProfile.objects.get(id=business_id)
        product = Product.objects.get(id=product_id, business_profile=business_profile)
        product.delete()
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Product deleted successful",
        }
        return Response(response_data, status=status.HTTP_200_OK)

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

    def put(self, request):
    
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
        
class OrderView(APIView):
    def get(self, request, order_id=None):
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                response_data = {
                    "status": status.HTTP_200_OK, 
                    "message": "Order retrieved successfully",
                    "data": serializer.data}
                return Response(
                    response_data,
                    status=status.HTTP_200_OK,
                )
            except Order.DoesNotExist:
                return Response({"status": status.HTTP_404_NOT_FOUND, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        response_data =  {
            "status": status.HTTP_200_OK, 
            "message": "Orders retrieved successfully", 
            "data": serializer.data}
        return Response(
           response_data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(
                {"status": status.HTTP_200_OK, "message": "Order created successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": status.HTTP_200_OK, "message": "Order updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"status": status.HTTP_200_OK, "message": "Order deleted successfully"}, status=status.HTTP_200_OK)