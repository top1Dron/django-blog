from django.urls import path
from app import views

app_name='app'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('rubric/<int:rubric_id>/', views.PostsByRubricListView.as_view(), name='by_rubric'),
]
