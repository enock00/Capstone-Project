from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    organizer =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title