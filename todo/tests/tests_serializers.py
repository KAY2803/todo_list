from django.contrib.auth.models import User
from django.core import serializers
from django.test import TestCase

from todo import serializers
from todo.models import ToDoList, Comment


class TestSerializers(TestCase):
    """Класс для тестирования сериализаторов"""

    note_attributes = None
    note = None
    comment_attributes = None
    comment = None

    @classmethod
    def setUpTestData(cls):
        """Классовый метод создания тестовой базы"""
        test_user_1 = User.objects.create(username="test_user_1", password="fake_password1", )

        cls.note_attributes = {
            'note': 'print name',
            'author': test_user_1,
            'status': 1,
            'importance': True,
            'public': True
        }

        cls.serializer_data_note = {
            'note': 'print name',
            'author': 1,
            'status': 1,
            'importance': True,
            'public': True
        }

        cls.note = ToDoList.objects.create(**cls.note_attributes)
        cls.serializer_note = serializers.NoteSerializer(instance=cls.note)

        cls.comment_attributes = {
            'comment': 'new comment',
            'note': cls.note,
            'author': test_user_1,
        }

        cls.serializer_data_comment = {
            'comment': 'new comment',
            'note': 1,
            'author': 1
        }

        cls.comment = Comment.objects.create(**cls.comment_attributes)
        cls.serializer_comment = serializers.CommentSerializer(instance=cls.comment)

    def test_NoteSerializer_keys(self):
        """Тест сериализатора модели ToDoList по ключам"""
        data = self.serializer_note.data
        self.assertCountEqual(data.keys(), ['id', 'note', 'author', 'status', 'importance', 'public', 'note_date'])

    def test_NoteSerializer_note(self):
        """Тест сериализатора модели ToDoList по значению"""
        data = self.serializer_note.data
        self.assertEqual(data['note'], self.note_attributes['note'])

    def test_NoteSerializer_status(self):
        """Тест сериализатора модели ToDoList по статусу"""
        data = self.serializer_note.data
        self.assertTrue(str(data['status']).isdigit())
        self.assertTrue(1 <= data['status'] <= 3)

    def test_CommentSerializer_keys(self):
        """Тест сериализатора модели Comment по ключам"""
        data = self.serializer_comment.data
        exp = data.keys()
        self.assertCountEqual(data.keys(), ['id', 'comment', 'note', 'author'])

    def test_CommentSerializer_values(self):
        """Тест сериализатора модели Comment по значению"""
        data = self.serializer_comment.data
        exp = data['comment']
        act = self.comment_attributes['comment']
        self.assertEqual(exp, act)

    def test_validation_CommentSerializer(self):
        """Тест сериализатора модели Comment на валидацию"""
        test_user_2 = User.objects.create(username="test_user_2", password="fake_password2", )
        note = self.serializer_note.data
        note['public'] = False
        comment = Comment.objects.create(comment='new comment', note=note, author=test_user_2)
        data_comment = serializers.NoteSerializer(instance=comment)
        exp = data_comment['note']
        act = self.comment_attributes['note']
        # todo как проверить валидность?
        self.assertEqual(exp, act)