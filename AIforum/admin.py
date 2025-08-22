from django.contrib import admin
from .models import Topic, Post

class TopicAdmin(admin.ModelAdmin):
    filter_horizontal = ('authorized_agents',) 

admin.site.register(Topic, TopicAdmin)
admin.site.register(Post)
