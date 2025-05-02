from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from profiles.models import Profile, Role
from .models import Task, TaskComment


@login_required
def index_view(request):
    return redirect('/tasks/')


class TaskListView(ListView):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        if profile.position == "Bosh muhandis o'rinbosari":
            tasks = Task.objects.filter(author=profile).exclude(status='completed').exclude(archived=True).order_by('deadline')

        else:
            tasks = Task.objects.filter(performers=profile).exclude(status='completed').exclude(archived=True).order_by('deadline')

        exclude_role_names = ['tchzg',]
        performers = Profile.objects.filter(~Q(roles__name__in=exclude_role_names))
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
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
                key = 'Muddatsiz'

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
            messages.success(request, 'Topshiriq muvaffaqiyatli yaratildi!')

    return redirect('/tasks')


def delete_task_veiw(request, task_id):
    task = Task.objects.get(id=task_id)
    task.archived = True
    task.save()
    return redirect('/tasks')


def task_comment_view(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        TaskComment.objects.create(
            author=request.user.profile,
            task=task,
            comment=comment)
    return redirect('/tasks/')

