# import from django
from django.shortcuts import render

# import from rest_framework
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
# import from apps
from .models import PaymentMethod, BusinessProfile, VerificationBadge
from .serializers import PaymentMethodSerializer, BusinessProfileSerializer, VerificationBadgeSerializer



class BusinessProfileListAPIView(APIView): # get all business profiles list
    
    def get(self, request, *args):
        queryset = BusinessProfile.objects.filter(is_active=True)
        response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'data': BusinessProfileSerializer(queryset, many=True).data
            }
        return Response(response_data)

class BusinessProfileAPIView(APIView): # get and create business profile for single user
    def get(self, request, *args, **kwargs):
        queryset = BusinessProfile.objects.filter(user=self.request.user)
        if queryset is None:
            response_data = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Business profile not found',
                'data': None
            }
        else:
            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'data': BusinessProfileSerializer(queryset, many=True).data
            }
        return Response(response_data)
    def post(self, request, *args,**kwargs):
        serializer = BusinessProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            
            response_data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Business profile created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PaymentMethodAPIView(APIView):

    def get(self, request, *args,**kwargs):
        queryset = PaymentMethod.objects.filter(user=self.request.user)
        if queryset is None:
            response_data = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Payment method not found',
                'data': None
            }
        else:
            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'data': PaymentMethodSerializer(queryset, many=True).data
            }
        return Response(response_data)
    def post(self, request, *args, **kwargs):
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            flag = serializer.save(user=self.request.user)
            business = BusinessProfile.objects.filter(user = self.request.user).first()
            print('business', business)
            if business:
                flag.business_profile = business
                flag.is_active = True
                flag.save()

            response_data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Payment method created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationBadgeAPIView(APIView):
    
    def post(self, request):
        pass