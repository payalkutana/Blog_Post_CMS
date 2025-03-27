from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

# #Update Django User Model
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.username
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    created_on = models.DateField(auto_now=True)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        return f"Post {self.post} is liked by {self.user}"