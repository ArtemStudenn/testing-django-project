# news/tests/test_logic.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):
    LOGIN_URL = reverse('users:login')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')
    HOME_URL = reverse('notes:home')
    ADD_URL = reverse('notes:add')
    LIST_URL = reverse('notes:list')
    SUCCESS_URL = reverse('notes:success')
    EDIT_URL = reverse('notes:edit', args=('slug',))
    DETAIL_URL = reverse('notes:detail', args=('slug',))
    DELETE_URL = reverse('notes:delete', args=('slug',))

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Мимо Крокодил')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='slug', author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new_slug'
        }

    def test_anonymous_user_cant_create_note(self):
        notes_count = Note.objects.count()
        self.client.post(self.ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count(), notes_count)

    def test_user_can_create_note(self):
        notes_count = Note.objects.count()
        self.author_client.post(self.ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count(), notes_count + 1)
        note = Note.objects.last()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_not_unique_slug(self):
        notes_count = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        form = response.context['form']
        self.assertFormError(form, 'slug', errors=(self.note.slug + WARNING))
        notes_count = Note.objects.count()
        self.assertEqual(Note.objects.count(), notes_count)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        self.author_client.post(self.ADD_URL, data=self.form_data)
        new_note = Note.objects.last()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        self.author_client.delete(self.DELETE_URL)
        self.assertEqual(Note.objects.count(), notes_count - 1)

    def test_other_user_cant_delete_note(self):
        notes_count = Note.objects.count()
        self.client.force_login(self.reader)
        response = self.client.delete(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count)

    def test_author_can_edit_note(self):
        self.author_client.post(self.EDIT_URL, data=self.form_data)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, self.form_data['title'])
        self.assertEqual(edited_note.text, self.form_data['text'])
        self.assertEqual(edited_note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        self.client.force_login(self.reader)
        response = self.client.post(self.EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        not_edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(not_edited_note.title, self.note.title)
        self.assertEqual(not_edited_note.text, self.note.text)
        self.assertEqual(not_edited_note.slug, self.note.slug)
