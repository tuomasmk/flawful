from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.db import connection

import sqlite3
import json

from .models import Todo

# Create your views here.

@login_required
def index(request):
    
    todos = Todo.objects.order_by('id')
    users = User.objects.filter(~Q(username=request.user.username)).order_by('username')
    return render(request, 'todos/index.html', {'items': todos, 
    'users': users})

@login_required
def search(request):
    content = request.POST.get('content').strip()
    dbname = connection.settings_dict['NAME']
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    response = cursor.execute("SELECT content FROM todos_todo WHERE content LIKE '%%%s%%'" % (content)).fetchall()
    todos = []
    if response is not None:
        for content in response:
            todos.append(Todo(content=content[0]))
    url = request.POST.get('url').strip()
    return render(request, 'todos/search.html', {'items': todos, 'url': url})

@login_required
def add(request):
    content = request.POST.get('content').strip()
    if len(content) > 0:
        todo = Todo(content = content, owner = request.user)
        todo.save()
        return redirect('/todos/')

@csrf_exempt
def delete(request):
    id = request.POST.get('todo_id')
    Todo.objects.filter(id=id).delete()
    return redirect('/todos/')

@login_required
def clear(request):
    user = request.user
    Todo.objects.filter(owner=user).delete()
    return redirect('/todos/')

