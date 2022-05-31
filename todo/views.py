from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission

from todo.models import ToDoList
from todo import serializers
from todo import permissions


class NoteListCreateAPIView(generics.ListCreateAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(author=self.request.user) | Q(public=True))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer


class NoteDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated & permissions.PublicOnly]

    def perform_update(self, serializer):
        author = self.get_object().author_id
        user = self.request.user.id
        if author == user:
            serializer.save()
            return serializer
        raise PermissionError('Недостаточно прав для внесения изменений')

