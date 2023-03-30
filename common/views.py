from rest_framework import exceptions
from common.authentication import JwtAuthentication
from core.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password



class RegisterApiView(APIView):
    def post(self, request):

        data = request.data
        if data['password'] != data['password_confirmed']:
            raise exceptions.APIException("Passwords do not match")

        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=make_password(data['password'])
        )
        # sets the register user to be ambassador if the api is 'api/ambassador
        # else makes the user admin
        # data['is_ambassador'] = 'api/ambassador' in request.path
        serializer = UserSerializer(user, many=False)
        # serializer.is_valid(raise_exception=True)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        login_password = data['password']
        user = User.objects.filter(email=email).first()
        if user is None or user.password != login_password:
            raise exceptions.AuthenticationFailed("Invalid user Credentials")

        # scope = 'ambassador' if 'api/ambassador' in request.path else 'admin'

        token = JwtAuthentication().generate_jwt_token(user_id=user.id)
        # token = JwtAuthentication().generate_jwt_token(user_id=user.id, scope=scope)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        # print(user.password + "==== PRINTED PASSWORD")
        response.data = {'message': 'success'}
        return response
    
    
class UserApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# NB: Logout => just remove the cookie using the response
class LogoutApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, _):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {'message': 'success'}
        return response


class ProfileInfoApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        # partial = True means we only update some fields
        # in this case: first_name, last_name and email
        serializer = UserSerializer(user, data=request.data, many=False, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordUpdateApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        if data['password'] != data['password_confirmed']:
            raise exceptions.APIException("Password do not match")
        user.set_password(data['password'])
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


