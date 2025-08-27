from rest_framework import serializers
from .models import Event, Comment
from django.utils import timezone
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
     
     organizer =  serializers.ReadOnlyField(source="organizer.username")

     class Meta:
          model = Event

          fields = [
               'title',
               'description',
               'location',
               'date_time',
               'organizer',
               'capacity',
               'location',
               'created_date'
               
               ]
          read_only_fields = ["organizer", "created_at"]

          def validate_date_time(self, value):
               if value < timezone.now():
                    raise serializers.ValidationError("Event can not be in the past.")
               return value
          
class UserSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True)

     class Meta:
          model = User

          fields = [
               'id',
               'username',
               'email',
               'password'
          ]
     def create(self, validated_data):
          user = User(
               username=validated_data["username"],
               email=validated_data.get("email"),
          )
          user.set_password(validated_data["password"])
          user.save()
          return User

class CommentSerializer(serializers.ModelSerializer):
     user_name = serializers.ReadOnlyField(source="user.username")

     class Meta:
          model = Comment

          fields = [
               'event',
               'user',
               'text',
               'created_at'
          ]

          read_only_fields = ('user', 'created_at')
          