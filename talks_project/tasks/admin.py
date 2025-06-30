from django.contrib import admin
from .models import Task, Comment

class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('title', 'description', 'priority', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'description')

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
