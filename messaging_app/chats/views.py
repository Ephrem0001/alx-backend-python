from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically add the requesting user as one of the participants.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter messages by conversation ID.
        Example: /api/messages/?conversation=<conversation_id>
        """
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        """
        Attach the authenticated user as the sender.
        """
        serializer.save(sender=self.request.user)
