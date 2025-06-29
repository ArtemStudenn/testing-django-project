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
    USERS_SIGNUP,
    NOTES_ADD_REDIRECT,
    NOTES_DELETE_REDIRECT,
    NOTES_DETAIL_REDIRECT,
    NOTES_EDIT_REDIRECT,
    NOTES_LIST_REDIRECT,
    NOTES_SUCCESS_REDIRECT
)


class TestRoutes(TestBase):
    def test_pages_availability(self):
        ways = (
            (NOTES_ADD, self.reader_client.get, HTTPStatus.OK),
            (NOTES_DELETE, self.author_client.get, HTTPStatus.OK),
            (NOTES_DELETE, self.reader_client.get, HTTPStatus.NOT_FOUND),
            (NOTES_DETAIL, self.author_client.get, HTTPStatus.OK),
            (NOTES_DETAIL, self.reader_client.get, HTTPStatus.NOT_FOUND),
            (NOTES_EDIT, self.author_client.get, HTTPStatus.OK),
            (NOTES_EDIT, self.reader_client.get, HTTPStatus.NOT_FOUND),
            (NOTES_HOME, self.author_client.get, HTTPStatus.OK),
            (NOTES_LIST, self.reader_client.get, HTTPStatus.OK),
            (NOTES_SUCCESS, self.reader_client.get, HTTPStatus.OK),
            (USERS_LOGIN, self.client.get, HTTPStatus.OK),
            (USERS_LOGOUT, self.client.post, HTTPStatus.OK),
            (USERS_SIGNUP, self.client.get, HTTPStatus.OK),
            (NOTES_ADD_REDIRECT, self.client.get, HTTPStatus.OK),
            (NOTES_DELETE_REDIRECT, self.client.get, HTTPStatus.OK),
            (NOTES_DETAIL_REDIRECT, self.client.get, HTTPStatus.OK),
            (NOTES_EDIT_REDIRECT, self.client.get, HTTPStatus.OK),
            (NOTES_LIST_REDIRECT, self.client.get, HTTPStatus.OK),
            (NOTES_SUCCESS_REDIRECT, self.client.get, HTTPStatus.OK),
        )
        for url, user_method, expected_status in ways:
            with self.subTest(
                url=url,
                user_method=user_method,
                expected_status=expected_status
            ):
                self.assertEqual(user_method(url).status_code, expected_status)

    def test_redirects(self):
        ways = (
            (NOTES_ADD, NOTES_ADD_REDIRECT),
            (NOTES_DELETE, NOTES_DELETE_REDIRECT),
            (NOTES_DETAIL, NOTES_DETAIL_REDIRECT),
            (NOTES_EDIT, NOTES_EDIT_REDIRECT),
            (NOTES_LIST, NOTES_LIST_REDIRECT),
            (NOTES_SUCCESS, NOTES_SUCCESS_REDIRECT),
        )
        for url, url_redirect in ways:
            with self.subTest(url=url, url_redirect=url_redirect):
                self.assertRedirects(self.client.get(url), url_redirect)
