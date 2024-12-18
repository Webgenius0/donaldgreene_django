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
    def get(self, request,business_id=None, *args, **kwargs):
        if business_id:
            queryset = BusinessProfile.objects.filter(id=business_id, user=self.request.user).first()
            if queryset:
                response_data = {
                    'status': status.HTTP_200_OK,
                    'message': 'Success',
                    'data': BusinessProfileSerializer(queryset).data
                }
                return Response(response_data)
            else:
                response_data = {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Business profile not found',
                    'data': None
                }
                return Response(response_data)
        queryset = BusinessProfile.objects.filter(user=self.request.user)
        if not queryset.exists():
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
        business_data = request.data.get('business_profile', {})
        payment_data = request.data.get('payment_method', {})

        business_serializer = BusinessProfileSerializer(data=business_data)
        payment_serializer = PaymentMethodSerializer(data=payment_data)

        if business_serializer.is_valid() and payment_serializer.is_valid():
            business_profile = business_serializer.save(user=self.request.user)
            payment_method = payment_serializer.save(user=self.request.user)
            if payment_method:
                payment_method.business_profile = business_profile 
                payment_method.save()

            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Business profile and payment method created successfully',
                'data': {
                    'business_profile': business_serializer.data,
                    # 'payment_method': payment_serializer.data
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response('success')
    
    def put(self, request,business_id=None, *args, **kwargs):
        if business_id:
            try:
                business_profile = BusinessProfile.objects.get(id=business_id, user=request.user)
            except BusinessProfile.DoesNotExist:
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'message': 'Business profile not found',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            business_data = request.data.pop('business_profile',None)
            business_serializer = BusinessProfileSerializer(business_profile, data=business_data, partial=True)
            payment_data = request.data.pop('payment_method', None)
            payment_serializer = PaymentMethodSerializer(data=payment_data, partial=True)
            # update business profile and payment method with existing data 
            if business_serializer.is_valid() and (payment_data is None or payment_serializer.is_valid()):
                business_serializer.save()
                if payment_data is not None:
                    payment_method = PaymentMethod.objects.filter(business_profile=business_profile).first()
                    payment_serializer.update(payment_method, payment_data)
                    payment_method.save()

                response_data = {
                    'status': status.HTTP_200_OK,
                    'message': 'Business profile updated successfully',
                    'data': business_serializer.data
                }
                return Response(response_data)
    def delete(self, request,business_id,*args,**kwargs):
        business_profile = BusinessProfile.objects.get(id=business_id, user=self.request.user)
        business_profile.delete()
        response_data = {
            'status': status.HTTP_200_OK,
           'message': 'Business profile deleted successfully',
            'data': None
        }
        return Response(response_data)
    
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