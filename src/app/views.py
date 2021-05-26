import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView
from app import utils
from app import forms
from app.models import Rubric, Post


logger = logging.getLogger(__name__)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = forms.PostForm
    success_url = reverse_lazy('app:index')
    template_name = 'app/post_create.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post_detail.html'

    def get_object(self) -> Post:
        try:
            post = utils.get_post_by_slug(slug=self.kwargs.get('slug'))
        except Post.DoesNotExist:
            return Http404('Post not found.')
        return post

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['rubrics'] = utils.get_all_rubrics()
        if not self.request.user.is_authenticated:
            context['login_form'] = forms.LoginForm()
            context['signup_form'] = forms.CustomUserCreationForm()
        if 'comment_form' in self.kwargs:
            context['comment_form'] = self.kwargs.get('comment_form')
        else:
            context['comment_form'] = forms.CommentForm()
        context['comments'] = utils.get_post_comments(self.object)
        context['comments_count'] = utils.get_comments_count(context['comments'])
        return context


@require_http_methods(['POST'])
def submit_post_comment(request, slug):
    post = utils.get_post_by_slug(slug)
    form = forms.CommentForm(request.POST)
    if form.is_valid():
        comment = utils.create_post_comment(
            comment_body=form.cleaned_data['body'], 
            post=post, 
            user=request.user)
    return redirect(reverse('app:post_detail', kwargs={'slug': slug}))



class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/index.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = utils.get_posts_with_shorten_body(posts=utils.get_all_posts())
        if 'date' in self.request.GET:
            queryset = utils.get_filtered_posts_by_date(
                posts=queryset, 
                published_filter=self.request.GET.get('date'))
        return queryset
    

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['rubrics'] = utils.get_all_rubrics()
        if not self.request.user.is_authenticated:
            context['login_form'] = forms.LoginForm()
            context['signup_form'] = forms.CustomUserCreationForm()
        return context


class PostsByRubricListView(PostListView):
    def get_queryset(self):
        queryset = utils.get_posts_with_shorten_body(
            posts=utils.get_posts_by_rubric(
                rubric_id=self.kwargs.get('rubric_id')))
        if 'date' in self.request.GET:
            queryset = utils.get_filtered_posts_by_date(
                posts=queryset, 
                published_filter=self.request.GET.get('date'))
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        try:
            context['rubric'] = utils.get_rubric_by_id(id=self.kwargs.get('rubric_id'))
        except Rubric.DoesNotExist:
            return Http404("Rubric doesn't exists.")
        context['title'] = context['rubric']
        return context


@require_http_methods(['POST'])
def api_login_user(request):
    errors = {}
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        user = utils.get_user_by_username(username)
        
        if user is not None and user.is_active == False:
            errors['invalid'] = 'User with inputed login is not active!'
        else:
            errors['invalid'] = 'User with inputed username and password is not exists!'
    return JsonResponse(errors)


def api_logout_user(request):
    logout(request)
    return redirect(reverse('app:index'))


@require_http_methods(['POST'])
def api_signup_user(request):
    body = json.loads(request.body)
    username = body.get('username')
    email = body.get('email')
    password1 = body.get('password1')
    password2 = body.get('password2')
    form = forms.CustomUserCreationForm(data={
        'username': username,
        'email': email,
        'password1': password1,
        'password2': password2
    })
    if form.is_valid():
        form.save()
        user = authenticate(
            request, 
            username=form.cleaned_data['username'], 
            password=form.cleaned_data['password1'])
        login(request, user)
    return JsonResponse(form.errors)


def api_search_post(request):
    search_title = request.GET.get('search_title')
    posts = {}
    logger.info(search_title)
    if search_title:
        posts = utils.get_filtered_posts(search_title)
    logger.info(posts)
    return JsonResponse(posts)