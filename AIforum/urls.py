from django.urls import path
from . import views

app_name = 'AIforum'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/new/', views.TopicCreateView.as_view(), name='topic_new'),
]