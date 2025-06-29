from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='slug', author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new_slug'
        }


NOTES_ADD = reverse('notes:add')
NOTES_DELETE = reverse('notes:delete', args=('slug',))
NOTES_DETAIL = reverse('notes:detail', args=('slug',))
NOTES_EDIT = reverse('notes:edit', args=('slug',))
NOTES_HOME = reverse('notes:home')
NOTES_LIST = reverse('notes:list')
NOTES_SUCCESS = reverse('notes:success')
USERS_LOGIN = reverse('users:login')
USERS_LOGOUT = reverse('users:logout')
USERS_SIGNUP = reverse('users:signup')
