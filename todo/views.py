from django.db.models import Q
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from todo import filters, permissions, serializers
from todo_list import settings_local
from todo.models import ToDoList, Comment


class NoteListCreateAPIView(generics.ListCreateAPIView):
    """Класс представления для вывода списка заметок и создания заметки"""
    queryset = ToDoList.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NoteFilter

    def get_queryset(self):
        """Переопределение метода get_queryset для получения доступа только к заметкам пользователя,
        а также заметкам других пользователей, которые отмечены как публичные"""
        queryset = super().get_queryset()
        return queryset.filter(Q(author=self.request.user) | Q(public=True))

    def perform_create(self, serializer):
        """Переопределение метода create для для передачи данных пользователя как автора заметки"""
        serializer.save(author=self.request.user)
        return serializer


class NoteDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс представления для вывода данных о конкретной заметке, ее изменения и удаления"""
    queryset = ToDoList.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated & permissions.GetPublicNote]

    def perform_update(self, serializer):
        """Переопределение метода update, которым изменения разрешено вносить только автору заметки"""
        author = self.get_object().author_id
        user = self.request.user.id
        if author == user:
            serializer.save()
            return serializer
        raise PermissionError('Недостаточно прав для внесения изменений')


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """Класс представления для вывода списка комментариев и создания комментария к заметке"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Переопределение метода create для ограничения создания комментария только к публичным заметкам"""
        serializer.save(author=self.request.user)
        return serializer


class AboutTemplateView(TemplateView):
    """Класс представления приветственной страницы"""
    template_name = 'todo/about.html'

    def get_context_data(self, **kwargs):
        """Вывод данных о версии сервера, сохраненных в settings_local на приветственной странице"""
        context = super().get_context_data(**kwargs)
        context['server'] = settings_local.SERVER_VERSION
        return context
