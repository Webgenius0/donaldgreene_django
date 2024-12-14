from rest_framework import serializers
from .models import BusinessProfile, PaymentMethod, VerificationBadge
from users.serializers import UserProfileSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"
    def create(self, *args, **kwargs):
        instance = super().create(*args, **kwargs)
        instance.user = self.context["request"].user
        instance.save()
        return instance


class VerificationBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationBadge
        fields = "__all__"


class BusinessProfileSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)
    verification_badge = VerificationBadgeSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = BusinessProfile
        fields = ['user','business_name', 'business_description','business_logo','payment_method','verification_badge']
