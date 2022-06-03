from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from todo.models import ToDoList

URL = '/api/v1/notes/'


class TestToDoViews(APITestCase):
    """Класс тестирования представления для модели ToDoList"""

    @classmethod
    def setUpTestData(cls):
        """Классовый метод для создания тестовой базы"""
        test_user_1 = User(username="test_user_1", password="fake_password1",)
        test_user_2 = User(username="test_user_2", password="fake_password2",)
        test_user_1, test_user_2 = User.objects.bulk_create([test_user_1, test_user_2])

        note_1 = ToDoList(note="note_1", author=test_user_1, status=1, importance=True, public=True)
        note_2 = ToDoList(note="note_2", author=test_user_1, status=2, importance=False, public=False)
        note_3 = ToDoList(note="note_3", author=test_user_2, status=3, importance=True, public=False)
        note_4 = ToDoList(note="note_4", author=test_user_2, status=1, importance=False, public=True)
        note_1, note_2, note_3, note_4 = ToDoList.objects.bulk_create([note_1, note_2, note_3, note_4])

        """ тест на получение списка заметок"""
    def test_get_NoteListCreateAPIView(self):
        # client.login(username="test_user_1", password="fake_password1")
        # todo как аутентифицировать клиента?
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(URL)
        queryset = ToDoList.objects.filter(Q(author=user.id) | Q(public=True))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(queryset.count(), len(response.data))

    """ тест на создание заметки в списке дел"""
    def test_post_NoteListCreateAPIView(self):
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'note': 'test post new note'}
        response = client.post(URL, data)
        queryset = ToDoList.objects.all()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(queryset.count(), 5)

    """ тест на получение данных о конкретной заметке"""
    def test_get_NoteDetailUpdateDeleteAPIView(self):
        pk = 4
        url = f'/api/v1/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    """ тест на проверку доступа к чужой непубличной заметке"""
    def test_get_permission_NoteDetailUpdateDeleteAPIView(self):
        pk = 3
        url = f'/api/v1/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    """тест на изменение заметки методом put - проверка прав на доступ к изменению"""
    def test_put_permission_NoteDetailUpdateDeleteAPIView(self):
        pk = 4
        url = f'/api/v1/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'note': 'update note 4', 'importance': True}
        response = client.put(url, data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # todo как проверить Permission error

    """тест на изменение заметки методом put"""
    def test_put_NoteDetailUpdateDeleteAPIView(self):
        pk = 1
        url = f'/api/v1/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'note': 'update note 1', 'importance': True}
        response = client.put(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('update note 1', response.data['note'])

    """тест на изменение заметки методом patch"""
    def test_patch_NoteDetailUpdateDeleteAPIView(self):
        pk = 2
        url = f'/api/v1/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'status': '3'}
        response = client.patch(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.data['status'])

    """тест на удаление заметки"""
    def test_del_NoteDetailUpdateDeleteAPIView(self):
        pk = 3
        url = f'/api/v1/notes/{pk}'
        user = User.objects.get(username='test_user_2')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(url)
        queryset = ToDoList.objects.all()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(queryset.count(), 3)