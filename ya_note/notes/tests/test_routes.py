from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
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
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='slug', author=cls.author
        )

    def test_pages_availability(self):
        urls = (
            self.HOME_URL, self.LOGIN_URL, self.LOGOUT_URL, self.SIGNUP_URL
        )
        for url in urls:
            if url == self.LOGOUT_URL:
                response = self.client.post(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
            else:
                with self.subTest(url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_client(self):
        urls = (self.ADD_URL, self.LIST_URL, self.SUCCESS_URL)
        self.client.force_login(self.reader)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        urls = (self.DELETE_URL, self.DETAIL_URL, self.EDIT_URL)
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for url in urls:
                with self.subTest(user=user, url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        urls = (
            self.ADD_URL,
            self.LIST_URL,
            self.SUCCESS_URL,
            self.DELETE_URL,
            self.DETAIL_URL,
            self.EDIT_URL
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
