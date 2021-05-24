from django.db.models import QuerySet
from app.models import Rubric, Post


def get_all_posts() -> QuerySet[Post]:
    return Post.objects.all()


def get_all_rubrics() -> QuerySet[Rubric]:
    return Rubric.objects.all()


def get_posts_by_rubric(rubric_id: int) -> QuerySet[Post]:
    return get_all_posts().filter(rubric=rubric_id)


def get_rubric_by_id(id):
    return Rubric.objects.get(pk=id)



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