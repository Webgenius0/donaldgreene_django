# import from django
from django.db import models
from django.conf import settings

# imort from rest_framework

# local imports
from users.models import User


class BusinessProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=250)
    business_description = models.TextField()
    business_logo = models.ImageField(blank=True, null=True, upload_to='business/business_logo/')
    is_active = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.business_name

ACCOUNT_TYPE = (
    ('General','General'),
    ('Premium','Premium'),
    ('VIP','VIP'),
)
class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='payments', blank=True, null=True)
    account_holder_fname = models.CharField(max_length=150)
    account_holder_lname = models.CharField(max_length=150)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE, default='General')
    account_number = models.CharField(max_length=80)
    routing_number = models.CharField(max_length=80)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_holder_fname} {self.account_holder_lname}"
    
    class Meta:
        verbose_name_plural = "Payment Methods"
        ordering = ['-created_at', '-updated_at']

BADGE = (
    ('Bronze', 'Bronze'),
    ('Silver', 'Silver'),
    ('Gold', 'Gold'),
    ('Platinum', 'Platinum'),

)
class Badge(models.Model):
    badge_name = models.CharField(max_length=10, choices=BADGE, blank=True, null=True)
    badge_description = models.TextField(blank=True, null=True)
    badge_logo = models.ImageField(blank=True, null=True, upload_to='business/badge_logo/')
    badge_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.badge_name}'
    
class VerificationBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='verifications', blank=True, null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='badges', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.business_profile.business_name} x {self.badge.badge_name}'


# class Wallet(models.Model):
#     pass 
