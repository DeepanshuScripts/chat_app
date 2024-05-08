from django.shortcuts import render
from chat.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.utils import generate_access_token, generate_refresh_token
from .models import UserProfile,UserOtp
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import random


# Create your views here.
class LoginApiView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        phone_number = data.get('phone_number')
        user,created = UserProfile.objects.get_or_create(phone_number=phone_number,username= phone_number)
        random_otp =   random.randint(100000, 999999)
        otp_info, created = UserOtp.objects.get_or_create(user=user)
        otp_info.otp = random_otp
        otp_info.save()
        return Response({'sucess':True,'otp':random_otp,'message':'Otp sent succesully'})


# Create your views here.
class OtpVerifyView(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            phone_number = data.get('phone_number')
            user = UserProfile.objects.get(phone_number=phone_number)
            otp_user = UserOtp.objects.get(user=user)
            if otp_user.otp== data.get('otp'):
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                serializered_data = {
                    'user_id' : user.id,
                    'access_token':access_token,
                    'refresh_token':refresh_token
                }
                return Response({"success": True, "message": "Token sent successfully", "data": serializered_data})
            else:
                return Response({"success": False, "message": "Otp Not Match.", "data": []})
        except UserProfile.DoesNotExist:
                return Response({"success": False, "message": "User does not exist", "data": []})
        except ValueError:
            return Response({"success": False, "message": "Please enter mobile number or email.", "data": []})




@api_view(['GET'])
def user_list(request, ):
    users = UserProfile.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = UserProfile.objects.all().order_by('username')
        serializer = UserSerializer(instance=users, many=True)
        return Response(serializer.data)