from django.contrib import admin
from unfold.admin import ModelAdmin

# import from app
from .models import BusinessProfile, VerificationBadge, PaymentMethod, Badge

@admin.register(BusinessProfile)
class BusinessProfileAdmin(ModelAdmin):
    list_display = ('user', 'business_name', 'business_description')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ('user', 'account_holder_fname','account_type') 

@admin.register(VerificationBadge)
class VerificationBadgeAdmin(ModelAdmin):
    pass

@admin.register(Badge)
class BadgeAdmin(ModelAdmin):
    list_display = ['badge_name', 'badge_price']