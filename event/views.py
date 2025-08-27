from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from .models import Event, Comment
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EventSerializer, CommentSerializer
from.permissions import IsorganizerOrReadOnly
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .serializers import RegistrationSerializer, LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)

            return Response({
                "message": "Login successful",
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsorganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_field = ['organizer']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date_time', 'created_date', 'capacity']
    ordering = ['date_time']

    def get_queryset(self):
        queryset = Event.objects.all()

        upcoming = self.request.query_params.get('upcoming', None)
        if upcoming and upcoming.lower() =='true':
            queryset = queryset.filter(date_time__gt=timezone.now())

        return queryset
        
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_pk = self.kwargs.get('event_pk')  
        if event_pk:
            return Comment.objects.filter(event_id=event_pk)
        return Comment.objects.all()

    def perform_create(self, serializer):
        event_pk = self.kwargs.get('event_pk')
        if event_pk:
            serializer.save(author=self.request.user, event_id=event_pk)
        else:
            serializer.save(author=self.request.user)