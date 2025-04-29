from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib import messages
from profiles.models import Profile, Role
from .models import Task


def index_view(request):
    return redirect('/tasks/')


class TaskListView(ListView):
    def get(self, request, *args, **kwargs):
        exclude_role_names = ['tchzg',]
        performers = Profile.objects.filter(~Q(roles__name__in=exclude_role_names))

        # profile = request.user.profile

        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        tasks = Task.objects.all().exclude(status='completed').order_by('deadline')

        grouped_tasks = {}

        for task in tasks:
            deadline_date = task.deadline
            if deadline_date == today:
                key = 'Bugun'
            elif deadline_date == tomorrow:
                key = 'Ertaga'
            elif deadline_date:
                key = deadline_date.strftime('%d.%m.%Y')
            else:
                key = 'Muddatsiz'  # deadline belgilanmagan topshiriqlar uchun

            if key not in grouped_tasks:
                grouped_tasks[key] = []
            grouped_tasks[key].append(task)

        return render(request, 'tasks/tasks.html', {'grouped_tasks': grouped_tasks, "performers": performers})














@csrf_exempt
def create_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        started = datetime.strptime(request.POST.get('started'), "%Y-%m-%d").date()
        deadline = datetime.strptime(request.POST.get('deadline'), "%Y-%m-%d").date()
        degree = request.POST.get('degree')
        performer_ids = request.POST.get('performers')

        # author = request.user.profiles
        author = Profile.objects.get(id=2)

        task = Task.objects.create(
            author=author,
            title=title,
            description=description,
            status='assigned',
            started=started or None,
            deadline=deadline or None,
            degree=degree or None,
        )

        if performer_ids:
            performers = Profile.objects.filter(id__in=performer_ids)
            task.performers.set(performers)
            messages.success(request, 'Task muvaffaqiyatli yaratildi!')

    return redirect('/tasks')


def delete_task_veiw(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/tasks')

