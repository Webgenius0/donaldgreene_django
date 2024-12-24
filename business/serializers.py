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
    # verifications = VerificationBadgeSerializer(read_only=True, many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        # depth = 1

    # def create(self, validated_data):
    #     print('validating data', validated_data)
    #     payment_data = validated_data.pop('payments', [])
    #     print('payment data', payment_data)
    #     business_logo = self.context['request'].FILES.get('business_logo')

    #     # Create the BusinessProfile instance
    #     business_profile = BusinessProfile.objects.create(
    #         user=self.context['request'].user,
    #         business_logo=business_logo,
    #         **validated_data
    #     )

    #     # Create PaymentMethod instances
    #     for payment in payment_data:
    #         PaymentMethod.objects.create(business_profile=business_profile, **payment)

    #     return business_profile

class CombineSerializer(serializers.Serializer):
    business_profile = BusinessProfileSerializer()
    payment_method = PaymentMethodSerializer()
    # verification_badge = VerificationBadgeSerializer()
    def create(self, validated_data):
        print('validated_data', validated_data)
        request = self.context.get('request')
        user = request.user 

        business_data = validated_data.pop('business_profile')
        payment_data = validated_data.pop('payment_method')

        print('business_data', business_data)
        print('payment_data', payment_data)

        # business_logo = request.FILES.get('business_profile.business_logo')
        business_profile = BusinessProfile.objects.create(
            user=user,
            **business_data
        )
        payment_data['user'] = user 
        payment_data['business_profile'] = business_profile 
        payment_method = PaymentMethod.objects.create(**payment_data)
        return { 'business_profile': business_profile, 'payment_method': payment_method }
    
    def update(self, instance, validated_data):
        business_profile_data = validated_data.get('business_profile',{})
        payment_method_data = validated_data.get('payment_method', {})

        for attr, value in business_profile_data.items(): 
            setattr(instance['business_profile'], attr, value)
        instance['business_profile'].save()

        for attr, value in payment_method_data.items():
            setattr(instance['payment_method'], attr, value)
        instance['payment_method'].save()

        return {
                'business_profile': instance['business_profile'], 
                'payment_method': instance['payment_method'] 
            }

