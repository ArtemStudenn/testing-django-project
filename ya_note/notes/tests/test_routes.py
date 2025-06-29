from http import HTTPStatus

from .base import (
    TestBase,
    NOTES_ADD,
    NOTES_DELETE,
    NOTES_DETAIL,
    NOTES_EDIT,
    NOTES_HOME,
    NOTES_LIST,
    NOTES_SUCCESS,
    USERS_LOGIN,
    USERS_LOGOUT,
    USERS_SIGNUP
)


class TestRoutes(TestBase):
    def test_pages_availability(self):
        ways = (
            (NOTES_ADD, self.reader_client, HTTPStatus.OK),
            (NOTES_DELETE, self.author_client, HTTPStatus.OK),
            (NOTES_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (NOTES_DETAIL, self.author_client, HTTPStatus.OK),
            (NOTES_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (NOTES_EDIT, self.author_client, HTTPStatus.OK),
            (NOTES_EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (NOTES_HOME, self.author_client, HTTPStatus.OK),
            (NOTES_LIST, self.reader_client, HTTPStatus.OK),
            (NOTES_SUCCESS, self.reader_client, HTTPStatus.OK),
            (USERS_LOGIN, self.client, HTTPStatus.OK),
            (USERS_LOGOUT, self.client, HTTPStatus.OK),
            (USERS_SIGNUP, self.client, HTTPStatus.OK),
        )
        for url, user, expected_status in ways:
            with self.subTest(
                url=url, user=user, expected_status=expected_status
            ):
                if url == USERS_LOGOUT:
                    response = user.post(url)
                else:
                    response = user.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects(self):
        urls = (
            NOTES_ADD,
            NOTES_DELETE,
            NOTES_DETAIL,
            NOTES_EDIT,
            NOTES_LIST,
            NOTES_SUCCESS
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url), f'{USERS_LOGIN}?next={url}'
                )
