from django.contrib import admin
from .models import Board, Post, Topic

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', '__str__', 'created_at')
    list_per_page = 10

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post, PostAdmin)