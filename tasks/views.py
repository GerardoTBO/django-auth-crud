from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
#from django.http import HttpResponse

# Create your views here.

def home(request):
    context = {
        'form': UserCreationForm,
    }
    return render(request, 'home.html', context)

def signup(request):

    if request.method == 'GET':        
        print('Enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                #return HttpResponse("Usuario creado satisfactoriamente")
                return redirect('tasks')
            except IntegrityError: # When a database restriction is set to unique
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya registrado'
                })
                
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Contraseñas no coinciden'
                })
    
@login_required
def tasks(request):
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks.html', context)

@login_required
def tasks_completed(request):
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Incorrect password or username'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):
    context = {
        'form': TaskForm,
    }
    if request.method == "GET":
        return render(request, 'create_task.html', context)
    else:
        try:
            form = TaskForm(request.POST)
            #print(form)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() # Save data to database
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please enter validated data'
            })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        context = {
            'task': task,
            'form': form,
        }
        return render(request, 'task_detail.html', context)
    else:
        try:
            form = TaskForm(request.POST, instance=task, user=request.user)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Please enter validated data'
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')