from django.urls import path

from .views import TaskListView, create_task

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create', create_task, name='create_task')
]