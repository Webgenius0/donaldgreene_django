from django.contrib import admin
from unfold.admin import ModelAdmin

# import from app
from .models import BusinessProfile, VerificationBadge, PaymentMethod


@admin.register(BusinessProfile)
class BusinessProfileAdmin(ModelAdmin):
    list_display = ('user', 'business_name', 'business_description', 'payment_method', 'verification_badge')

    def verification_badge(self, obj):
        return obj.verification_badge.badge_name if obj.verification_badge else None

@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ('user', 'account_holder_fname','account_type') 