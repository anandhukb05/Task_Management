from django.urls import path
from .views import dashboard, manage_users, manage_tasks, task_reports, admin_login, admin_logout



urlpatterns = [
    path('login/', admin_login),
    path('logout/', admin_logout),
    path('dashboard/', dashboard),
    path('users/', manage_users),
    path('tasks/', manage_tasks),
    path('reports/', task_reports)
]