from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, news_on_homepage, news_home):
    response = client.get(news_home)
    assert (
        response.context['object_list'].
        count() == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(client, news_on_homepage, news_home):
    all_dates = [news.date for news in client.get(news_home).
                 context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, comments_list, news_detail):
    assert 'news' in client.get(news_detail).context
    news = client.get(news_detail).context['news']
    all_timestamps = [comment.created for comment in news.comment_set.all()]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client, news_detail):
    assert 'form' not in client.get(news_detail).context


def test_authorized_client_has_form(author_client, news_detail):
    assert isinstance(
        author_client.get(news_detail).context.get('form'), CommentForm
    )
