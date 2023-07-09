from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.timezone import now
import json,ast
from asgiref.sync import sync_to_async

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

    def add_user(self,user_id):
        if self.is_valid():
            users = self.get_users()
            if user_id not in users:
                self.users['users'].append(user_id)
                self.save()
    def remove_user(self,user_id):
        if self.is_valid():
            users = self.get_users()
            if user_id in users:
                self.users['users'].remove(user_id)
                self.save()
    async def async_add_message(self,message_id):
        if self.is_valid():
            messages = self.get_messages()
            print(message_id not in messages)
            if message_id not in messages:
                self.messages['messages'].append(message_id)
                print(self.messages,"trying to save")
                await sync_to_async(self.save)()
                print('saved')
    def remove_message(self,message_id):
        if self.is_valid():
            messages = self.get_messages()
            if message_id in messages:
                self.messages['messages'].remove(message_id)
                self.save()
                

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
            return self.messages['messages'] or []
    
    async def async_fetch_messages(self):
        if self.is_valid():
            messages = []
            for message_id in self.get_messages():
                try:
                    message = await sync_to_async(Message.objects.get)(id=message_id)
                    messages.append(message)
                except Message.DoesNotExist:
                    pass
            return messages
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
    
    async def async_fetch_users(self):
        """
        Récupérer les utilisateurs de la discussion
        """
        if self.is_valid():
            users = []
            for user_id in self.get_users():
                try:
                    user = await sync_to_async(ChatUser.objects.get)(id=user_id)
                    users.append(user)
                except ChatUser.DoesNotExist:
                    pass
            return users
        return []


    
  

