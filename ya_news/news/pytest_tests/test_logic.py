from django.urls import reverse

from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(client, news):
    comments_count = Comment.objects.count()
    client.post(
        reverse('news:detail', args=(news.id,)), data={'text': 'Комментарий'}
    )
    assert comments_count == Comment.objects.count()


def test_user_can_create_comment(author_client, news, author):
    comments_count = Comment.objects.count()
    response = author_client.post(
        reverse('news:detail', args=(news.id,)), data={'text': 'Комментарий'}
    )
    assertRedirects(
        response, f'{reverse('news:detail', args=(news.id,))}#comments'
    )
    assert comments_count + 1 == Comment.objects.count()
    comment = Comment.objects.first()
    assert comment.text == 'Комментарий'
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news):
    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(
        reverse('news:detail', args=(news.id,)), data=bad_words_data
    )
    form = response.context['form']
    assertFormError(form=form, field='text', errors=WARNING)
    assert comments_count == Comment.objects.count()


def test_author_can_delete_comment(author_client, comment, news):
    comments_count = Comment.objects.count()
    response = author_client.delete(reverse('news:delete', args=(comment.id,)))
    assertRedirects(
        response, f'{reverse('news:detail', args=(news.id,))}#comments'
    )
    assert comments_count - 1 == Comment.objects.count()


def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
    comments_count = Comment.objects.count()
    not_author_client.delete(reverse('news:delete', args=(comment.id,)))
    assert comments_count == Comment.objects.count()


def test_author_can_edit_comment(author_client, comment, news):
    response = author_client.post(
        reverse('news:edit', args=(comment.id,)),
        data={'text': 'Обновленный комментарий'}
    )
    assertRedirects(
        response, f'{reverse('news:detail', args=(news.id,))}#comments'
    )
    comment.refresh_from_db()
    assert comment.text == 'Обновленный комментарий'


def test_user_cant_edit_comment_of_another_user(not_author_client, comment):
    response = not_author_client.post(
        reverse('news:edit', args=(comment.id,)),
        data={'text': 'Обновленный комментарий'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'
