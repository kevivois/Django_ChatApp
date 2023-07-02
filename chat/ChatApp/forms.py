from django import forms
class ChatUserForm(forms.Form):
    class Meta:
        model = 'ChatUser'
        fields = ('email','username','password','hashtag')

class MessageForm(forms.Form):
    class Meta:
        model = 'Message'
        fields = ('id','discussion','user','content') 