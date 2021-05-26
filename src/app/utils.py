import datetime
import logging
import textwrap
from typing import Union
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

from django.contrib.auth.models import User
from django.db.models import QuerySet
from app.models import Comment, Rubric, Post


logger =  logging.getLogger(__name__)


def get_all_posts() -> QuerySet[Post]:
    return Post.objects.filter(status='PB').select_related('rubric')


def get_posts_with_shorten_body(posts: QuerySet[Post]) -> QuerySet[Post]:
    for post in posts:
        body = textwrap.shorten(dehtml(post.body), 300, placeholder='...')
        last_chars = body[-4:-13:-1][::-1]
        try:
            post.body = post.body[:post.body.index(last_chars)]
            post.body = textwrap.shorten(post.body, len(post.body) - 20, placeholder='...')
        except ValueError:
            post.body = textwrap.shorten(post.body, 300, placeholder='...')
    return posts


def get_post_by_slug(slug)-> Post:
    return Post.objects.get(slug=slug)


def get_posts_by_title_part(search_title:str) -> dict:
    return get_all_posts().filter(title__icontains=search_title)


def get_filtered_posts(search_title:str) -> dict:
    return {post.slug: post.title for post in get_posts_by_title_part(search_title)}


def get_post_comments(post: Post) -> QuerySet[Comment]:
    return Comment.objects.filter(post=post)


def get_comments_count(comments_or_post: Union[QuerySet[Comment], Post], /) -> int:
    if isinstance(comments_or_post, Post):
        return get_post_comments(comments_or_post).count()
    elif isinstance(comments_or_post, QuerySet[Comment]):
        return comments_or_post.count()
    else:
        raise TypeError('get_comments_count function only accepts a parameter of Union[QuerySet[Comment], Post]')


def create_post_comment(comment_body:str, post: Post, user: User) -> Comment:
    comment = Comment.objects.create(
        post=post,
        author=user,
        body=comment_body)
    return comment


def get_comment(comment_pk):
    return Comment.objects.get(pk=comment_pk)


def delete_post_comment(comment_pk: int) -> None:
    comment: Comment = get_comment(comment_pk)
    comment.delete()


def get_filtered_posts_by_date(posts: QuerySet[Post], published_filter) -> QuerySet[Post]:
    if published_filter == 'today':
        posts = posts.filter(
            published__day=datetime.date.today().day,
            published__month=datetime.date.today().month, 
            published__year=datetime.date.today().year )
    elif published_filter == 'last_seven_days':
        posts = posts.filter(
            published__gte=datetime.datetime.now()-datetime.timedelta(days=7))
    elif published_filter == 'this_month':
        posts = posts.filter(
            published__month=datetime.date.today().month, 
            published__year=datetime.date.today().year)
    elif published_filter == 'this_year':
        posts = posts.filter(published__year=datetime.date.today().year)
    elif published_filter == 'previous_year':
        posts = posts.filter(published__year=datetime.date.today().year-1)
    return get_posts_with_shorten_body(posts)



def get_all_rubrics() -> QuerySet[Rubric]:
    return Rubric.objects.all()


def get_posts_by_rubric(rubric_id: int) -> QuerySet[Post]:
    return get_all_posts().filter(rubric=rubric_id)


def get_rubric_by_id(id):
    return Rubric.objects.get(pk=id)


def get_user_by_username(username):
    try:
        user = User.objects.get(username=username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user


class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text