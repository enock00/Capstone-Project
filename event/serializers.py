from rest_framework import serializers
from .models import Event, Comment
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True, required=True)
     confirm_password = serializers.CharField(write_only=True, required=True)

     class Meta:
          model = User
          fields = ("username", "password", "confirm_password", "email")
          
     def validate(self, attrs):
          if attrs ["password"] != attrs["confirm_password"]:
               raise serializers.ValidationError({"Password":"Passwords does not match" })
          return attrs
     
     def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data

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
          