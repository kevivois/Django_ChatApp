from django.contrib import admin
from ChatApp.models import ChatUser,Message
# Register your models here.

admin.register(ChatUser,Message)
