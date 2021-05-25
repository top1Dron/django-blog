import datetime
import logging
import textwrap

from django.contrib.auth.models import User
from django.db.models import QuerySet
from app.models import Rubric, Post


logger =  logging.getLogger(__name__)


def get_all_posts() -> QuerySet[Post]:
    return Post.objects.all().select_related('rubric')


def get_posts_with_shorten_body(posts: QuerySet[Post]) -> QuerySet[Post]:
    for post in posts:
        post.body = textwrap.shorten(post.body, 300, placeholder='...')
    return posts


def get_filtered_posts_by_date(posts: QuerySet[Post], published_filter=None) -> QuerySet[Post]:
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



def get_context_with_pagination_settings(*, context: dict):
    '''
    return context with pagination settings
    maximum pages = 10
    '''

    if not context.get('is_paginated', False):
        return context

    paginator = context.get('paginator')
    num_pages = paginator.num_pages
    current_page = context.get('page_obj')
    page_no = current_page.number

    if num_pages <= 10 or page_no <= 6: 
        pages = [x for x in range(1, min(num_pages + 1, 11))]
    elif page_no > num_pages - 6:
        pages = [x for x in range(num_pages - 9, num_pages + 1)]
    else:
        pages = [x for x in range(page_no - 5, page_no + 5)]

    context.update({'pages': pages})
    return context