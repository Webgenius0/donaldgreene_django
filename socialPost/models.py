from django.db import models
from users.models import User
import uuid
# Create your models here.

class SocialPost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    react = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    share = models.BooleanField(null=True, blank=True)
    like = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


