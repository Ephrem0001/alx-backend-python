from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Expect participants to be passed in request data as list of user IDs
        participants_ids = self.request.data.get('participants', [])
        conversation = serializer.save()
        if participants_ids:
            users = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.set(users)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        sender_id = self.request.data.get('sender')
        conversation_id = self.request.data.get('conversation')
        sender = get_object_or_404(User, user_id=sender_id)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        serializer.save(sender=sender, conversation=conversation)
