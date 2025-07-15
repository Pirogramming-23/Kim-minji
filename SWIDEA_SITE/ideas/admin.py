from django.contrib import admin
from .models import Idea, IdeaStar

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'devtool', 'interest', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('devtool',)

@admin.register(IdeaStar)
class IdeaStarAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea')
    search_fields = ('user__username', 'idea__title')
