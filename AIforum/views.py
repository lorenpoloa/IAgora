from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Post
from django.views.generic import CreateView
from django.urls import reverse_lazy

def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'AIforum/topic_list.html', {'topics': topics})

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    posts = topic.posts.all()
    return render(request, 'AIforum/topic_detail.html', {'topic': topic, 'posts': posts})

class TopicCreateView(CreateView):
    model = Topic
    fields = ['title', 'description']
    template_name = 'AIforum/topic_form.html'
    success_url = reverse_lazy('AIforum:topic_list')  # Redirect to topic list after creation
