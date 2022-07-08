from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserSetPasswordSerializer, CustomUserStatusSerializer


class CustomUserList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    # retrieve list of all users
    def get(self, request):
        CustomUsers = CustomUser.objects.all()
        serializer = CustomUserSerializer(CustomUsers, many=True)
        return Response(serializer.data)

    # post new user data, using custom method to create password-less user
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            from datetime import datetime
            birthdate = datetime.strptime(serializer.data.get('birthdate'), "%Y-%m-%d").date()
            if serializer.data.get('gender').upper() == 'MALE':
                gender = 1
            elif serializer.data.get('gender').upper() == 'FEMALE':
                gender = 0

            # Programmatically create new user without password arg (does not raise any exceptions)
            # the database field password contain an empty string (empty password)
            # empty password can be set with PasswordResetView
            user_obj = CustomUser.objects.create(
                first_name=serializer.data.get('first_name'),
                last_name=serializer.data.get('last_name'),
                country_code=serializer.data.get('country_code'),
                phone_number=serializer.data.get('phone_number'),
                gender=gender,
                birthdate=birthdate,
                # although avatar available in serializer.data before validation, after validation it is None
                # so a work around is getting it from request (all validations are in model)
                avatar=request.data.get('avatar'),
                email=serializer.data.get('email'),
                username=serializer.data.get('last_name').replace(' ', '-')
            )
            serializer = CustomUserSerializer(user_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserSetPassword(APIView):
    def post(self, request):
        serializer = CustomUserSetPasswordSerializer(data=request.data)
        print('### request.data == ', request.data)
        print('### serialized input data == ', serializer)
        if serializer.is_valid():
            print('### serialerzer is vaild & it data == ', serializer.data)
            user = serializer.create(serializer.data)
            if user:
                # Token.objects.create(user=instance)
                token, created = Token.objects.get_or_create(user=user)
                data = {'new_token': token.key, } if created else {'token': token.key, }
                return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserSetStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CustomUserStatusSerializer(data=request.data)
        if serializer.is_valid():
            status_obj = serializer.create(serializer.data, request=request)
            if status_obj:
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Hand Shaking successfully Completed',
                    'data': []
                }
                return Response(response)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
