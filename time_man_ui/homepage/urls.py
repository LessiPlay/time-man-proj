from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/<int:task_id>', views.showTaskDetail, name='task_detail'),
]
