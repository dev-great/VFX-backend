from django.db import models

# Create your models here.

class NotificationPost(models.Model):
    
    title = models.CharField(max_length=300)
    body=models.CharField(max_length=500,blank=True, null=True)
    date= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)


    def __str__(self):
        return self.body[:100]