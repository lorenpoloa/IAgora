from django.shortcuts import render
from .models import Agent

def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'agents/agent_list.html', {'agents': agents})
