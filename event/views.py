from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters
from .models import Event, Comment
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EventSerializer, CommentSerializer
from.permissions import IsorganizerOrReadOnly
from django.utils import timezone

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