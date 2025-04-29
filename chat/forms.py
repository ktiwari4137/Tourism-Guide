from django import forms
from .models import Message, ChatRoom

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your message here...',
                'class': 'form-control'
            })
        }
        labels = {
            'content': ''
        }

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'participants']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter chat room name'
            }),
            'participants': forms.SelectMultiple(attrs={
                'class': 'form-control'
            })
        } 