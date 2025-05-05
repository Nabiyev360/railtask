from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from profiles.models import Profile
from .models import Task, TaskComment
from .services import send_task_tg_users


@login_required
def index_view(request):
    return redirect('/tasks/')


from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render

class TaskListView(ListView):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        tasks = Task.objects.filter(archived=False)

        if profile.position == "Bosh muhandis o'rinbosari":
            tasks = tasks.filter(author=profile)
        else:
            tasks = tasks.filter(performers=profile)

        status = request.GET.get('status')
        expired_tasks = tasks.filter(deadline__lt=timezone.now())
        if status == 'expired':
            tasks = expired_tasks
        elif status in ['in_progress', 'completed']:
            tasks = tasks.filter(status=status)

        # Grouping
        grouped_tasks = {}
        for task in tasks.order_by('deadline'):
            if task.deadline.date() == today:
                key = 'Bugun'
            elif task.deadline.date() == tomorrow:
                key = 'Ertaga'
            elif task.deadline:
                key = task.deadline.strftime('%d.%m.%Y')
            else:
                key = 'Muddatsiz'
            grouped_tasks.setdefault(key, []).append(task)

        # Performers ro‘yxati (filtrlangan)
        exclude_role_names = ['tchzg']
        performers = Profile.objects.exclude(roles__name__in=exclude_role_names)

        return render(request, 'tasks/tasks.html', {
            'grouped_tasks': grouped_tasks,
            'performers': performers,
            'expired_tasks': expired_tasks,
        })



@csrf_exempt
def create_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = datetime.fromisoformat(request.POST.get('deadline'))
        degree = request.POST.get('degree')
        performer_ids = request.POST.getlist('performers')
        author = request.user.profile

        task = Task.objects.create(
            author=author,
            title=title,
            description=description,
            status='in_progress',
            deadline=deadline or None,
            degree=degree or None,
        )

        if performer_ids:
            performers = Profile.objects.filter(id__in=performer_ids)
            task.performers.set(performers)
            messages.success(request, 'Topshiriq muvaffaqiyatli yaratildi!')
            send_task_tg_users(task)
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