from django.http import Http404
from django.views.generic import ListView
from app import utils
from app.models import Rubric, Post


class PostListView(ListView):
    model = Post
    queryset = utils.get_all_posts()
    context_object_name = 'posts'
    template_name = 'app/index.html'
    paginate_by = 3
    

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['rubrics'] = utils.get_all_rubrics()
        return context


class PostsByRubricListView(PostListView):
    def get_queryset(self):
        queryset = utils.get_posts_by_rubric(rubric_id=self.kwargs.get('rubric_id'))
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        try:
            context['rubric'] = utils.get_rubric_by_id(id=self.kwargs.get('rubric_id'))
        except Rubric.DoesNotExist:
            return Http404("Rubric doesn't exists.")
        context['title'] = context['rubric']
        return context