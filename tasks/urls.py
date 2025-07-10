# tasks/urls.py
from django.urls import path
from .views import (
    TaskList, TaskCreate, TaskUpdate, TaskDelete, 
    statistics_view, toggle_task_complete
)

urlpatterns = [
    path('', TaskList.as_view(), name='task_list'),
    path('statistics/', statistics_view, name='statistics'),
    path('create/', TaskCreate.as_view(), name='task_create'),
    path('update/<int:pk>/', TaskUpdate.as_view(), name='task_update'),
    path('delete/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
    path('toggle/<int:pk>/', toggle_task_complete, name='toggle_task'),
]