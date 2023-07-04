from django.contrib import admin
from ChatApp.models import ChatUser,Message,Discussion
# Register your models here.

admin.site.register(ChatUser)
admin.site.register(Message)
admin.site.register(Discussion)