from django.urls import path

from .views import TaskListView, create_task_view, delete_task_veiw, task_comment_view, update_status_view

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create', create_task_view, name='create_task'),
    path('delete/<int:task_id>', delete_task_veiw, name='delete_task'),
    path('update-status/<int:task_id>', update_status_view, name='update_status'),
    path('task_comment_view/<int:task_id>', task_comment_view, name='task_comment'),

    path('workers', TaskListView.as_view())
]
