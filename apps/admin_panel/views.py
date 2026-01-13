from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.users.models import User
from apps.tasks.models import Task
from django.contrib.auth import authenticate, login, logout


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['admin', 'superadmin']:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'superadmin':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user and user.role in ['admin', 'superadmin']:
            login(request, user)
            return redirect('/admin/dashboard/')
        return render(request, 'admin/login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def admin_logout(request):
    logout(request)
    return redirect('/admin/login/')



@login_required
@admin_required
def dashboard(request):
    if request.user.role == 'superadmin':
        users_count = User.objects.count()
        tasks = Task.objects.all()
    else:
        users_count = User.objects.filter(assigned_admin=request.user).count()
        tasks = Task.objects.filter(assigned_to__assigned_admin=request.user)

    context = {
        'users_count': users_count,
        'tasks_count': tasks.count(),
        'completed_tasks': tasks.filter(status='completed').count()
    }

    return render(request, 'dashboard.html', context)



@login_required
@superadmin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})



@login_required
@admin_required
def manage_tasks(request):
    if request.user.role == 'superadmin':
        tasks = Task.objects.select_related('assigned_to').all()
    else:
        tasks = Task.objects.select_related('assigned_to').filter(
            assigned_to__assigned_admin=request.user
        )

    return render(request, 'tasks.html', {'tasks': tasks})



@login_required
@admin_required
def task_reports(request):
    if request.user.role == 'superadmin':
        tasks = Task.objects.filter(status='completed')
    else:
        tasks = Task.objects.filter(
            status='completed',
            assigned_to__assigned_admin=request.user
        )

    return render(request, 'reports.html', {'tasks': tasks})
