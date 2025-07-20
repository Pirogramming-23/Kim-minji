from django.contrib import admin
from .models import Post, Comment, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

from .models import Profile

admin.site.register(Profile)