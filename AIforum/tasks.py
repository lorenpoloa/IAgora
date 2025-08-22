from celery import shared_task
from .models import Topic, Post
from agents.models import Agent
from agents.utils import generate_response
import random, re
from django.utils import timezone


# Clean up the response text, removing any <think> tags
def clean_response(text: str) -> str:
    # Quita bloques <think>...</think> (multilínea)
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()




@shared_task
def check_and_respond():
    """
    Checks for topics without posts or posts without responses and generates a response using Ollama.
    """

    now = timezone.now()

    # Find topics without any posts
    topics_without_posts = Topic.objects.filter(posts__isnull=True)
    for topic in topics_without_posts:
        authorized_agents = topic.authorized_agents.all()
        if authorized_agents:
            agent = random.choice(authorized_agents)
            previous_posts = []  # No previous posts for a new topic
            response_content = generate_response(agent, topic, previous_posts)
            new_post = Post(topic=topic, author=agent, content=response_content)
            new_post.save()
            print(f"Generated initial post for topic: {topic.title} by agent: {agent.name}")

    # Find topics with posts but without recent responses (e.g., last post older than 24 hours)
    cutoff_time = now - timezone.timedelta(minutes=1)
    topics_with_stale_posts = Topic.objects.filter(posts__created_at__lt=cutoff_time).distinct()
    for topic in topics_with_stale_posts:
        # Filtrar por número de posts (< 15)
        if topic.posts.count() >= 15:
            print(f"Skipping topic '{topic.title}' (has {topic.posts.count()} posts, limit is 15)")
            continue


        authorized_agents = topic.authorized_agents.all()
        if authorized_agents:
            agent = random.choice(authorized_agents)
            previous_posts = topic.posts.order_by('created_at')
            context = ""
            ##############################
            ### Debugging context size###
            #############################
            for post in previous_posts:
                context += f"{post.content}\n"
            context_size_bytes = len(context.encode("utf-8"))
            print("=" * 60)
            print(f"[DEBUG] Tamaño del contexto: {len(context)} caracteres, {context_size_bytes} bytes")
            print("=" * 60)
            ###############################
            ##############################

            response_content = generate_response(agent, topic, previous_posts)
            response_text = clean_response(response_content)
            new_post = Post(topic=topic, author=agent, content=response_text)
            new_post.save()
            print(f"Generated response for topic: {topic.title} by agent: {agent.name}")



@shared_task
def test_task():
    print(">>> Test task ejecutada correctamente")
