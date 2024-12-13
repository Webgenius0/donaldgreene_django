from django.db import models
from users.models import User

# Create your models here.

class DayStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class DayStoryComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_story = models.ForeignKey(DayStory, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.day_story.title}'
    

class DayStoryLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_story = models.ForeignKey(DayStory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Like by {self.user.username} on {self.day_story.title}'


class DayStoryShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_story = models.ForeignKey(DayStory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Share by {self.user.username} on {self.day_story.title}'
    
