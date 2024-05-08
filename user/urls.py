from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='user_login'),
    path('otp_verify/', OtpVerifyView.as_view(), name='otp_verify'),
    path('', user_list, name='user_list'),
    path('user_list/', UserView.as_view(), name='user_list')
]