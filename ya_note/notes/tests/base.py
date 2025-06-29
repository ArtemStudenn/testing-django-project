from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


NOTE_SLUG = 'slug'


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
            title='Заголовок', text='Текст', slug=NOTE_SLUG, author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new_slug'
        }


NOTES_ADD = reverse('notes:add')
NOTES_DELETE = reverse('notes:delete', args=(NOTE_SLUG,))
NOTES_DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))
NOTES_EDIT = reverse('notes:edit', args=(NOTE_SLUG,))
NOTES_HOME = reverse('notes:home')
NOTES_LIST = reverse('notes:list')
NOTES_SUCCESS = reverse('notes:success')
USERS_LOGIN = reverse('users:login')
USERS_LOGOUT = reverse('users:logout')
USERS_SIGNUP = reverse('users:signup')

NOTES_ADD_REDIRECT = f'{USERS_LOGIN}?next={NOTES_ADD}'
NOTES_DELETE_REDIRECT = f'{USERS_LOGIN}?next={NOTES_DELETE}'
NOTES_DETAIL_REDIRECT = f'{USERS_LOGIN}?next={NOTES_DETAIL}'
NOTES_EDIT_REDIRECT = f'{USERS_LOGIN}?next={NOTES_EDIT}'
NOTES_LIST_REDIRECT = f'{USERS_LOGIN}?next={NOTES_LIST}'
NOTES_SUCCESS_REDIRECT = f'{USERS_LOGIN}?next={NOTES_SUCCESS}'
