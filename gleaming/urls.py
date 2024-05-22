from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/',          admin.site.urls),
    path('',                views.home,         name='home'),
    path('signup/',         views.signup,       name='signup'),

    path('tasks/',          views.tasks,        name='tasks'),
    path('tasks_completed/',views.tasks_completed, name='tasks_completed'),
    
    path('tasks/create/',   views.create_task,  name='create_task'),

    # un id sera guardado en esta variable: task_id
    path('tasks/<int:task_id>/',   views.task_detail,  name='task_detail'),

    # un id sera guardado en esta variable: task_id
    path('tasks_completed/<int:task_id>/',   views.task_detail,  name='task_detail'),

    # para marcar tarea como completada
    path('tasks/<int:task_id>/complete',   views.complete_task,  name='complete_task'),

    # para deletear
    path('tasks/<int:task_id>/delete',   views.delete_task,  name='delete_task'),

    path('logout/',         views.signout,      name='logout'),
    path('signin/',         views.signin,       name='signin')
]
# Example of explanation for create_task.html
#   Path				: 'tasks/create/' para que luzca como una url
#   views.create_task	: La function a ejecutar cuando visite esta url
#   name='create_task'	: El nombre de la ruta
