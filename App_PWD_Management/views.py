from rest_framework.views import APIView
from .serializers import UserSerializer,UserCreatePasswordSerializer,UserGetPasswordSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User,UserPassword
import jwt,datetime


#SIGN UP AND LOGIN
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #.decode('utf-8')

        # return Response({
        #     'jwt':token
        #     })

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):

    def get(self, request):
 
        token = request.COOKIES.get('jwt')
        

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response 

#CRUD FOR PASSWORDS

class UserCreatePasswordView(APIView):

    def post(self,request):
        token = request.COOKIES.get('jwt')
        

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
    
        serializer = UserCreatePasswordSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(cust=user)


        return Response(serializer.data)

class UserGetPasswordView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt')
        

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        view=UserPassword.objects.filter(cust=user)
        serializer=UserGetPasswordSerializer(view,many=True)
        return Response(serializer.data)

class UserUpdatePasswordView(APIView):
    
    def patch(self, request,pk):
        obj = UserPassword.objects.get(id=pk)
        data = request.data
        obj.pwd = data.get("pwd", obj.pwd)
        obj.save()
        serializer = UserCreatePasswordSerializer(obj)

        return Response(serializer.data)


class UserDeletePasswordView(APIView):    
    def delete(self,request, pk):
        task=UserPassword.objects.get(id=pk)
        task.delete()
        return Response('Item succsesfully delete!')

