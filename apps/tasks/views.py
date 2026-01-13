from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer, TaskCompleteSerializer
from apps.users.restriction import IsUser, IsAdminOrSuperAdmin

# Create your views here.


# GET /tasks
class UserTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

# PUT /tasks/{id}
class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskCompleteSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

# GET /tasks/{id}/report
class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]

    def get_queryset(self):
        return Task.objects.filter(status='completed')
