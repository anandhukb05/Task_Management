from django.urls import path
from .views import UserTaskListView, TaskUpdateView, TaskReportView

urlpatterns = [
    path('tasks/', UserTaskListView.as_view()),
    path('tasks/<int:pk>/', TaskUpdateView.as_view()),
    path('tasks/<int:pk>/report/', TaskReportView.as_view()),
]
