from django.urls import path
from app import views

app_name='app'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('by-rubric/<int:rubric_id>/', views.PostsByRubricListView.as_view(), name='by_rubric'),
    path('login/', views.api_login_user, name='login'),
    path('logout/', views.api_logout_user, name='logout'),
    path('signup/', views.api_signup_user, name='signup'),
]
