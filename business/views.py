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



class BusinessProfileListAPIView(generics.ListAPIView):
    queryset = BusinessProfile.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'data': BusinessProfileSerializer(queryset, many=True).data
            }
        )

class BusinessProfileAPIView(generics.ListCreateAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return BusinessProfile.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

class PaymentMethodAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payment_method = PaymentMethod.objects.filter(user=request.user).first()
        if payment_method:
            serializer = PaymentMethodSerializer(payment_method)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'success',
                    'data': serializer.data
                }
            )
        else:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Payment method not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )