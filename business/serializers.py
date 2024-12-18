from rest_framework import serializers
from .models import BusinessProfile, PaymentMethod, VerificationBadge
from users.serializers import UserProfileSerializer

# verification badge serializers
class VerificationBadgeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = VerificationBadge
        fields = "__all__"
        read_only_fields = ['business_profile']

# payment methods serializers
class PaymentMethodSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PaymentMethod
        fields = "__all__"
        read_only_fields = ['business_profile']

# business profile serializers
class BusinessProfileSerializer(serializers.ModelSerializer):
    payments = PaymentMethodSerializer(read_only=True, many=True)
    verifications = VerificationBadgeSerializer(read_only=True, many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = BusinessProfile
        fields = ['id','user','business_name', 'business_description','business_logo', 'payments', 'verifications']
        # depth = 1

