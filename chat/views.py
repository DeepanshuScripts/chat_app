from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import UserProfile
from .serializers import ConversationListSerializer, ConversationSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


def index(request):
    return render(request,'base.html',{})


# def room(request,room_name):
#     return render(request,'chatroom.html',{
#         'room_name':room_name
#     })

    
class CreateChatRoom(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request,):
        data = request.data
        username = data.pop('phone_number')
        try:
            participant = UserProfile.objects.get(phone_number=username)
            conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                                    Q(initiator=participant, receiver=request.user))
            if conversation.exists():
                return redirect(reverse('get_conversation', args=(conversation[0].id,)))

            else:
                conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
                return Response(ConversationSerializer(instance=conversation).data)
        except UserProfile.DoesNotExist:
            return Response({'message': 'You cannot chat with a non existent user'})


class GetChatRoom(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def get(request, convo_id):
        conversation = Conversation.objects.filter(id=convo_id)
        if not conversation.exists():
            return Response({'message': 'Conversation does not exist'})
        else:
            serializer = ConversationSerializer(instance=conversation[0])
            return Response(serializer.data)
    
# get chat rooms for request.user
@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
