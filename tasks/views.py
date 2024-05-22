# from django.shortcuts import render
# #from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

# # Create your views here.
# def helloworld(request):
# #   return HttpResponse('<h1>Hola Moises - Exito</h1>')

# #   necesito recibir el parametro request y enviar pagina html: signup.html
#     #return render(request, 'signup.html')

#     #puedo crear diccionario para mandar la informacion
#     # title = 'Hola soy titulo'  
#     # return render(request, 'signup.html', {
#     #     'mytitle': title
#     # })

#     return render(request, 'signup.html', {
#         'form': UserCreationForm
#     })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']: 
            # print(request.POST)
            # print('Obteniendo datos')
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1']
                    )
                user.save()
                login(request, user)
                #return HttpResponse('User created sucessfully')
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Password do not match'
                })
    # return render(request, 'signup.html', {
    #     'form': UserCreationForm
    # })

@login_required
def tasks(request):
    #tasks = Task.objects.all()  # devuelve todas las tareas de la base de datos
    #tasks = Task.objects.filter(user=request.user)  # la propiedad user debe ser igual user del request
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)  # Datecompleted null
    return render(request, 'tasks.html', {'tasks':tasks})  # paso dato al Front 

    #return render(request, 'tasks.html')  

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')  
    return render(request, 'tasks.html', {'tasks':tasks}) 

@login_required
def create_task(request):
    if request.method == 'GET':   #cuando recibo por primera vez el formulario
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:                         # viene el formulario de nuevo pero con datos
        # no me esta enviando por el metodo GET sino a travez de un button : Save
        # print(request.POST)   # pongo print para verificar que tengo los datos

        # aqui recibo los datos y se los paso a la clase TaskForm y el va a generar por mi un formulario         
        # un test para verlo :
        # form = TaskForm(request.POST)
        # print(form)

        # utilisare el formulario para grabar los datos
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)   # solo quiero que devuelva los datos, por eso pongo commit False
            new_task.user = request.user         # Como no estoy entregando el usuario, genera un error. al moverlo desde request no hay problema
            #print(new_task)                     # esto es una nueva tarea , la vere por consola
            new_task.save()                      # una vez lo guardo, no quiero que me renderize, le dire que me redireccione a pagina tasks
            # return render(request, 'create_task.html', {
            #     'form': TaskForm
            # })
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                        'form': TaskForm,
                        'error': 'Please provide valida data'
                    })
        except IntegrityError:
            return render(request, 'create_task.html', {
                        'form': TaskForm,
                        'error': 'Hay un Error de integridad'
                    })

@login_required
def task_detail(request, task_id):
    # #print(task_id)

    # # El task_id me sirve para consultar. Desde el modelo Task utilisare object y obtener un dato
    # # le digo que busque el dato donde el primary key = task_id
    # task = get_object_or_404(Task, pk=task_id)
    # form = TaskForm(instance=task)   # Llama instance con el valor de la tarea (task)

    # #return render(request, 'task_detail.html')
    # #return render(request, 'task_detail.html', {'task': task})

    # # Le pasamos el valor al Front
    # return render(request, 'task_detail.html', {'task': task, 'form': form})

    if request.method == 'GET':
        # task = get_object_or_404(Task, pk=task_id)
        # No debe modificar tarea que no le pertenece : user=request.user
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)   # Llama instance con el valor de la tarea (task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # No debe modificar tarea que no le pertenece : user=request.user
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 
                          'task_detail.html', 
                          {'task': task, 
                           'form': form, 
                           'error': "Error Updating task"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, 
                            username=request.POST['username'], 
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            "error": 'Username or Password Incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
    

    