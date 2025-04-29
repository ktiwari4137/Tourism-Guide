from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .forms import MessageForm

User = get_user_model()

# Create your views here.

class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat/chatroom_list.html'
    context_object_name = 'chatrooms'

    def get_queryset(self):
        return self.request.user.chatrooms.all()

class ChatRoomDetailView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat/chatroom_detail.html'
    context_object_name = 'chatroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all()
        context['form'] = MessageForm()
        return context

    def get_queryset(self):
        return self.request.user.chatrooms.all()

class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    fields = ['name', 'participants']
    template_name = 'chat/chatroom_create.html'
    success_url = reverse_lazy('chat:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Chat room created successfully!')
        return super().form_valid(form)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'chat/message_create.html'

    def form_valid(self, form):
        chatroom = get_object_or_404(ChatRoom, pk=self.kwargs['pk'])
        form.instance.chatroom = chatroom
        form.instance.sender = self.request.user
        messages.success(self.request, 'Message sent successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat:detail', kwargs={'pk': self.kwargs['pk']})
