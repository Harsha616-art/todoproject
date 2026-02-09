from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import datetime

# List all tasks
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Create new task
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        # Handle empty or invalid date
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
            except ValueError:
                due_date_obj = None
        else:
            due_date_obj = None

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date_obj,
            priority=priority
        )
        return redirect('task_list')

    return render(request, 'tasks/task_create.html')

# Toggle completed status
def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

# Delete a task
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

# Edit / Update a task
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        # Handle empty or invalid date
        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            except ValueError:
                task.due_date = None
        else:
            task.due_date = None

        task.priority = request.POST.get('priority')
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/task_edit.html', {'task': task})
