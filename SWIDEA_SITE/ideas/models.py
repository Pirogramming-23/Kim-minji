from django.db import models
from django.contrib.auth.models import User
from devtools.models import DevTool  # devtools 앱의 DevTool 모델

class Idea(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='idea_images/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'idea')  # 한 유저가 한 아이디어에 한 번만 찜 가능

    def __str__(self):
        return f"{self.user.username} ❤️ {self.idea.title}"
