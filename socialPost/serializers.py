from rest_framework import serializers
from .models import SocialPost

class SocialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPost
        fields = '__all__'
        read_only_fields = ['user']
