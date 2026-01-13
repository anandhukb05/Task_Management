from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from tasks.models import Task

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')

@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/users.html', {'users': users})

@login_required
def manage_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'admin/tasks.html', {'tasks': tasks})

@login_required
def task_reports(request):
    tasks = Task.objects.filter(status='completed')
    return render(request, 'admin/reports.html', {'tasks': tasks})
