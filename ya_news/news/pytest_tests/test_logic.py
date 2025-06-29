from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

BAD_WORDS_DATA = [
    {'text':
     f'Какой-то текст, {bad_word}, еще текст'
     } for bad_word in BAD_WORDS
]
COMMENT_DATA = {'text': 'Комментарий'}


def test_anonymous_user_cant_create_comment(client, news_detail):
    client.post(news_detail, data=COMMENT_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author_client, news_detail, news, author, comments_redirect
):
    assertRedirects(
        author_client.post(news_detail, data=COMMENT_DATA),
        comments_redirect
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize('bad_words', BAD_WORDS_DATA)
def test_user_cant_use_bad_words(author_client, news_detail, bad_words):
    assertFormError(
        form=author_client.post(news_detail, data=bad_words).context['form'],
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client, news_delete, comments_redirect
):
    assertRedirects(
        author_client.delete(news_delete), comments_redirect
    )
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, news_delete, comment
):
    not_deleted_comment = Comment.objects.get(id=comment.id)
    not_author_client.delete(news_delete)
    assert Comment.objects.count() == 1
    assert not_deleted_comment.text == comment.text
    assert not_deleted_comment.news == comment.news
    assert not_deleted_comment.author == comment.author


def test_author_can_edit_comment(
        author_client, comment, comments_redirect, news_edit
):
    assertRedirects(
        author_client.post(news_edit, data=COMMENT_DATA),
        comments_redirect
    )
    edited_comment = Comment.objects.get(id=comment.id)
    assert edited_comment.text == COMMENT_DATA['text']
    assert edited_comment.news == comment.news
    assert edited_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, news_edit
):
    assert not_author_client.post(
        news_edit, data=COMMENT_DATA
    ).status_code == HTTPStatus.NOT_FOUND
    not_edited_comment = Comment.objects.get()
    assert not_edited_comment.text == comment.text
    assert not_edited_comment.news == comment.news
    assert not_edited_comment.author == comment.author
