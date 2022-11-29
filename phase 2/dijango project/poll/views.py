from django.shortcuts import render
from django.shortcuts import redirect

from .forms import CreatePollForm
from .models import Poll
import json
import subprocess
import os
from datetime import datetime
s=''
e=''

def home(request):
    global s
    global e
    if request.method == "POST":
        s = request.POST['start']
        e = request.POST['end']

        return redirect('analytics')
    polls = Poll.objects.all()

    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

def analytics(request):
    if request.method == 'GET':
        form = CreatePollForm(request.GET)
    global s
    global e
    # all_data = [{'name':'s10','cpu':s, 'disk':555, 'ram':666, 'time':10, 'count': 11},
    # {'name':'s10','cpu':e, 'disk':555, 'ram':666, 'time':10, 'count': 11},
    # {'name':'s10','cpu':123, 'disk':555, 'ram':666, 'time':10, 'count': 11}]
    # return render(request, 'poll/analytics.html', {'all_data': all_data})

    start = datetime.strptime(s,'%Y-%d-%m').date()
    start = start.strftime('%m-%d-%Y')

    end = datetime.strptime(e, '%Y-%d-%m').date()
    end = end.strftime('%m-%d-%Y')

    folder_name = 'server/health_data'
    file_range = ['python', './server/map_reduce.py']

    for file_dir in os.listdir(folder_name):
        print(file_dir)
        date = datetime.strptime(file_dir[:-5], '%m-%d-%Y').date()
        date = date.strftime('%m-%d-%Y')
        if date <= end and date >= start:
                file_range.append('./server/health_data/'+ str(date)+'.json')

    x = subprocess.check_output(file_range)  
    x = x.decode().replace('}\n{','},{')        
    x = '{"services":['+ x +']}'
    data = json.loads(x)
    return render(request, 'poll/analytics.html', {'all_data': data['services']})