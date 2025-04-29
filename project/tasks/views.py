from datetime import datetime

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
        tasks = Task.objects.all()
        # tasks = Task.objects.filter(author__id=request.user.profile.id)
        exclude_role_names = ['tchzg',]
        performers = Profile.objects.filter(~Q(roles__name__in=exclude_role_names))
        return render(request, "tasks/tasks.html", {"tasks": tasks, "performers": performers})

@csrf_exempt
def create_task_veiw(request):
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

