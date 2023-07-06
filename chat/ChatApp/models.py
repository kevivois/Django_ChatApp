from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.timezone import now
import json,ast

def default_uuid_value():
    return str(uuid.uuid4())

def default_json_messages_value():
    return {"messages":[]}
def default_json_users_value():
    return {"users":[]}

class ChatUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=default_uuid_value,db_index=True,unique=True)
    email = models.EmailField(max_length=254, unique=True,blank=False)
    username = models.CharField(max_length=255,unique=True,blank=False)
    password = models.CharField(max_length=255,blank=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    

class Message(Model):
    id = models.UUIDField(primary_key=True,default=default_uuid_value,db_index=True,unique=True)
    discussion = models.ForeignKey('Discussion',on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser,on_delete=models.SET_NULL,null=True) 
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)


class Discussion(Model):
    id = models.UUIDField(primary_key=True,default=default_uuid_value,db_index=True,unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    picture = models.ImageField()
    messages = models.JSONField(default=default_json_messages_value)
    users = models.JSONField(default=default_json_users_value)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        if self.name == '':
            print('no name')
            return False
        
        if self.users == '' or self.messages == '':
            print('no users or no messages')
            return False
        
        try:
            if type(self.users) != dict or type(self.messages) != dict:
                raise Exception('not dict')
            if 'users' not in self.users or 'messages' not in self.messages:
                raise Exception('not corrects properties')

        except Exception as e:
            print(e)
            return False
        return True
    def make_lists_valid(self):
        if not self.is_valid():
            if 'users' not in self.users:
                self.users = "{'users':[]}"
            if 'messages' not in self.messages:
                self.messages = "{'messages':[]}"
            self.save()
            return self

    def has_messages(self):
        if self.is_valid():
            if len(self.get_messages()) > 0:
                return True
        return False
    def has_users(self):
        if self.is_valid():
            if len(self.users['users']) > 0:
                return True
        return False
    
    def get_messages(self):
        if self.has_messages():
            return self.messages['messages']
        return []
    def get_users(self):
        if self.has_users():
            return self.users['users']
        return []
    
    def fetch_users(self):
        """
        Récupérer les utilisateurs de la discussion
        """
        if self.is_valid():
            users = []
            for user_id in self.get_users():
                try:
                    user = ChatUser.objects.get(id=user_id)
                    users.append(user)
                except ChatUser.DoesNotExist:
                    pass
            return users
        return []

    
  

