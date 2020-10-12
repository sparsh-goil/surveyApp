from django.shortcuts import render
from user_profile.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        content  = {
            'status': "Success!"
        }
        return Response(content)
        