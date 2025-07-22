from django.contrib import admin
from .models import Post, Comment, Like, Profile, PostImage  # PostImage 추가

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Profile)

# PostImage 등록
@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image')  # admin 페이지에서 id, post, image 컬럼 표시