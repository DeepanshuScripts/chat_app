from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:room_name>/',views.room, name='room'),

    #new urls
    path('create_chatroom/', views.CreateChatRoom.as_view(), name='create_conversation'),
    path('get_chatroom/<int:convo_id>/', views.GetChatRoom.as_view(), name='get_conversation'),
    path('', views.conversations, name='conversations')

]
