from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


NEWS_DELETE = pytest.lazy_fixture('news_delete')
NEWS_DETAIL = pytest.lazy_fixture('news_detail')
NEWS_EDIT = pytest.lazy_fixture('news_edit')
NEWS_HOME = pytest.lazy_fixture('news_home')
USERS_LOGIN = pytest.lazy_fixture('users_login')
USERS_SIGNUP = pytest.lazy_fixture('users_signup')

NEWS_DELETE_REDIRECT = pytest.lazy_fixture('news_delete_redirect')
NEWS_EDIT_REDIRECT = pytest.lazy_fixture('news_edit_redirect')

AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
CLIENT = pytest.lazy_fixture('client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')


def test_logout(client, users_logout):
    assert client.post(users_logout).status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'url, user, expected_status',
    (
        (NEWS_DELETE, AUTHOR_CLIENT, HTTPStatus.OK),
        (NEWS_DELETE, CLIENT, HTTPStatus.FOUND),
        (NEWS_DELETE, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (NEWS_DETAIL, CLIENT, HTTPStatus.OK),
        (NEWS_EDIT, AUTHOR_CLIENT, HTTPStatus.OK),
        (NEWS_EDIT, CLIENT, HTTPStatus.FOUND),
        (NEWS_EDIT, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (NEWS_HOME, CLIENT, HTTPStatus.OK),
        (USERS_LOGIN, CLIENT, HTTPStatus.OK),
        (USERS_SIGNUP, CLIENT, HTTPStatus.OK),
        (NEWS_DELETE_REDIRECT, AUTHOR_CLIENT, HTTPStatus.OK),
        (NEWS_EDIT_REDIRECT, AUTHOR_CLIENT, HTTPStatus.OK),
    )
)
def test_pages_availability_for_all_users(url, user, expected_status):
    assert user.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_redirect',
    (
        (NEWS_DELETE, NEWS_DELETE_REDIRECT),
        (NEWS_EDIT, NEWS_EDIT_REDIRECT)
    )
)
def test_redirects(client, url, expected_redirect):
    assertRedirects(client.get(url), expected_redirect)
