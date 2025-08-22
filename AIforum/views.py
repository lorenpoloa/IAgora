from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Post
from django.views.generic import CreateView
from django.urls import reverse_lazy
import markdown, bleach
from django.http import HttpResponse


def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'AIforum/topic_list.html', {'topics': topics})

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    posts = topic.posts.all()
     # Convertir Markdown de cada post a HTML
    for post in posts:
        html = markdown.markdown(post.content, extensions=['extra', 'codehilite'])
        # Limpiar HTML si quieres prevenir XSS
        post.content = html
    return render(request, 'AIforum/topic_detail.html', {'topic': topic, 'posts': posts})

class TopicCreateView(CreateView):
    model = Topic
    fields = ['title', 'description']
    template_name = 'AIforum/topic_form.html'
    success_url = reverse_lazy('AIforum:topic_list')  # Redirect to topic list after creation
