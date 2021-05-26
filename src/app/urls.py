from django.urls import path
from app import views

app_name='app'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('blog/by-rubric/<int:rubric_id>/', views.PostsByRubricListView.as_view(), name='by_rubric'),
    path('blog/create/', views.PostCreateView.as_view(), name='post_create'),
    path('blog/search-posts/', views.api_search_post, name='post_search'),
    path('blog/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('blog/<slug:slug>/delete-comment/<int:pk>/', views.delete_post_comment, name='delete_comment'),
    path('blog/<slug:slug>/submit-comment/', views.submit_post_comment, name='submit_comment'),
    path('login/', views.api_login_user, name='login'),
    path('logout/', views.api_logout_user, name='logout'),
    path('signup/', views.api_signup_user, name='signup'),
]
