from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.timezone import now


class ChatUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,db_index=True,unique=True)
    email = models.EmailField(max_length=254, unique=True,null=False,blank=False)
    username = models.CharField(max_length=255,unique=True,null=False,blank=False)
    password = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"User {str(self.id)}"
    

class Message(models.Model):
    id = models.UUIDField(db_index=True,primary_key=True,default=uuid.uuid4)
    discussion = models.ForeignKey('Discussion',on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser,on_delete=models.DO_NOTHING) 
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message {str(self.id)} from {self.user} : {self.content}"

class Discussion(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,db_index=True),
    title = models.CharField(max_length=255),
    description = models.CharField(max_length=500)
    picture = models.ImageField()
    messages = models.JSONField()
    users = models.JSONField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Discussion {str(self.id)}"

    
  

