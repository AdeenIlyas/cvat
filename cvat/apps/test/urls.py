from django.urls import path
from . import views

urlpatterns = [
    path('tasks/<int:task_id>/annotation_counts', views.annotation_counts, name='annotation_counts'),
]
