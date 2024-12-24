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
from rest_framework.parsers import FormParser,MultiPartParser
# import from apps
from .models import PaymentMethod, BusinessProfile, VerificationBadge
from .serializers import PaymentMethodSerializer, BusinessProfileSerializer, CombineSerializer



class BusinessProfileListAPIView(APIView): # get all business profiles list
    
    def get(self, request, *args):
        queryset = BusinessProfile.objects.filter(is_active=True)
        response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Retrive Business Profile Success',
                'data': BusinessProfileSerializer(queryset, many=True).data
            }
        return Response(response_data)

class BusinessProfileAPIView(APIView): # get and create business profile for single user

    parser_classes = [FormParser,MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,business_id=None, *args, **kwargs):
        if business_id:
            queryset = BusinessProfile.objects.filter(id=business_id, user=self.request.user).first()
            if queryset:
                response_data = {
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'message': 'Retrive Business Profile',
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
                'success': True,
                'message': 'Success',
                'data': BusinessProfileSerializer(queryset, many=True).data
            }
        return Response(response_data)
    def post(self, request, *args, **kwargs):

        # print('raw data', request.data)
       

        serializer = CombineSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save(user=request.user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Business profile created successfully",
                    'data': {
                        'business_profile': BusinessProfileSerializer(data['business_profile']).data, 
                        'payment_method': PaymentMethodSerializer(data['payment_method']).data 
                        }
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,business_id=None, *args, **kwargs):
        if business_id:
            try:
                business_profile = BusinessProfile.objects.get(id=business_id, user=request.user)
                payment_method = PaymentMethod.objects.filter(business_profile=business_profile, user=request.user).first()
            except BusinessProfile.DoesNotExist or PaymentMethod.DoesNotExist:
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'message': 'Business profile or Payment method not found',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = CombineSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                data = serializer.update(
                    instance={'business_profile': business_profile, 'payment_method': payment_method},
                    validated_data=serializer.validated_data
                )
                response_data = {
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'message': 'Business profile updated successfully',
                    'data': { 
                        'business_profile': BusinessProfileSerializer(data['business_profile']).data, 
                        'payment_method': PaymentMethodSerializer(data['payment_method']).data 
                        }
                }
                return Response(response_data)
            # update business profile and payment method with existing data 
            
    def delete(self, request,business_id,*args,**kwargs):
        business_profile = BusinessProfile.objects.get(id=business_id, user=self.request.user)
        business_profile.delete()
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
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
                'success': True,
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
                'success': True,
                'message': 'Payment method created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationBadgeAPIView(APIView):
    
    def post(self, request):
        pass