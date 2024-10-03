from django.db import models
from accounts.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE ,related_name='puser')
    image = models.ImageField(upload_to='post_image')
    caption = models.CharField(max_length=255)
    slug=models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.caption
    
    def likecounts(self):
        return self.pvots.count()

class Vote(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE,related_name='uvotes')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pvotes')
    
    def __str__(self):
        return f'{self.user} liked -> {self.post}'    
        
        
class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    
    def __str__(self):
        return self.user.username

class SaveMessage(models.Model):
    user_message = models.ForeignKey(UserMessage, on_delete=models.CASCADE, related_name='saved_messages')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user_message.user.username} - {self.post.slug}' 

class Relations(models.Model):
    from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='followers')
    to_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='following')
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.from_user} follow {self.to_user}'


    
class UserRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.from_user.username} requested {self.to_user.username}'
    