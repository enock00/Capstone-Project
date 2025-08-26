from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Event(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    organizer =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.date_time < timezone.now():

            raise ValidationError("Event can not be in the past")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.user.username} on {self.event.title} "
     