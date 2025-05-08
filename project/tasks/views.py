from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from profiles.models import Profile
from .models import Task, TaskComment
from .services import send_task_tg_users
from django.http import JsonResponse, Http404


@login_required
def index_view(request):
    return redirect('/tasks/')


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

        expired_tasks = tasks.filter(deadline__lt=timezone.now()).exclude(status='completed')

        counts = {
            "all": tasks.count(),
            "expired": expired_tasks.count(),
            "in_progress": tasks.filter(status='in_progress').count(),
            "completed": tasks.filter(status='completed').count(),

            "info": tasks.filter(degree='info').count(),
            "medium": tasks.filter(degree='medium').count(),
            "important": tasks.filter(degree='important').count(),
            "very_important": tasks.filter(degree='very_important').count(),
            "urgent": tasks.filter(degree='urgent').count(),
        }

        workers = Profile.objects.all().exclude(position="Bosh muhandis o'rinbosari")
        workers_task_count = {}
        for worker in workers:
            workers_task_count[worker] = tasks.filter(performers=worker).count()

        workers_task_count = dict(sorted(workers_task_count.items(), key=lambda item: item[1], reverse=True))   # sort by task count

        status = request.GET.get('status')
        degree = request.GET.get('degree')
        worker_id = request.GET.get('worker_id')
        if status == 'expired':
            tasks = expired_tasks
        elif status in ['in_progress', 'completed']:
            tasks = tasks.filter(status=status)
        elif degree:
            tasks = tasks.filter(degree=degree)
        elif worker_id:
            worker = Profile.objects.get(id=worker_id)
            tasks = tasks.filter(performers=worker)

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

        exclude_role_names = ['tchzg']
        performers = Profile.objects.exclude(roles__name__in=exclude_role_names)

        return render(request, 'tasks/tasks.html', {
            'grouped_tasks': grouped_tasks,
            'performers': performers,
            'expired_tasks': expired_tasks,
            'counts': counts,
            'workers_task_count': workers_task_count
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


def update_status_view(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.status == 'completed':
        task.status = 'in_progress'
    else:
        task.status = request.GET.get('status')
    task.save()
    return JsonResponse({'status': task.status})



def task_detail_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Topshiriq topilmadi")

    return JsonResponse({
        'title': task.title,
        'description': task.description,
        'deadline': task.deadline.strftime('%Y-%m-%dT%H:%M'),
        'degree': task.degree,
        'performers': list(task.performers.values_list('id', flat=True)),
    })

def edit_task_view(request, task_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        degree = request.POST.get('degree')
        performer_ids = request.POST.getlist('performers')


        task = Task.objects.get(id=task_id)
        task.title = title
        task.description = description
        task.deadline = deadline
        task.degree = degree
        task.performers = performer_ids
        task.save()
        send_task_tg_users(task)
    return redirect('/tasks/')


