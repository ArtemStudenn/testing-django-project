from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости'
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        text='Текст комментария',
        news=news,
        author=author
    )


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def news_on_homepage():
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_list(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def news_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def news_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def news_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def news_home():
    return reverse('news:home')


@pytest.fixture
def users_login():
    return reverse('users:login')


@pytest.fixture
def users_logout():
    return reverse('users:logout')


@pytest.fixture
def users_signup():
    return reverse('users:signup')


@pytest.fixture
def news_delete_redirect(users_login, news_delete):
    return f'{users_login}?next={news_delete}'


@pytest.fixture
def news_edit_redirect(users_login, news_edit):
    return f'{users_login}?next={news_edit}'
