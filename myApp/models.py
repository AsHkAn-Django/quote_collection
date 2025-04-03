from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Quote(models.Model):
    body = models.CharField(max_length=500)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=260)
    like_numbers = models.PositiveSmallIntegerField(default=0)
    
    def count_likes(self):
        counter = Like.objects.filter(quote=self).count()
        self.like_numbers = counter
        self.save()
        return counter

    def __str__(self):
        return f"{self.author}: {self.body[:50]}..."

    def get_absolute_url(self):
        return reverse('quote_detail', kwargs={'pk': self.pk})



class Comment(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"{self.author.username}: {self.body[:50]}..."
    
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Liked {self.quote.author} quote"
    
    
class SubComment(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='sub_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    sub_comment = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)