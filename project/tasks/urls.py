from django.urls import path

from .views import TaskListView, create_task_view, delete_task_veiw

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create', create_task_view, name='create_task'),
    path('delete/<int:task_id>', delete_task_veiw, name='delete_task')
]