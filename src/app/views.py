import json
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, forms as auth_forms
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse, request, JsonResponse
from django.shortcuts import redirect, reverse, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from app import utils
from app import forms
from app.models import Rubric, Post


logger = logging.getLogger(__name__)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/index.html'
    paginate_by = 3

    def get_queryset(self):
        return utils.get_posts_with_shorten_body(posts=utils.get_all_posts())
    

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