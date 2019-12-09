from rest_framework import generics,viewsets, generics, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view#para el decorador
from django.contrib.auth.models import User
from .serializers import UserSerializerWithToken, GetFullUserSerializer
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
# permission_classes = (permissions.IsAuthenticated,)
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class GetAllUserAndProfiles(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = GetFullUserSerializer

@api_view(['GET'])
def get_current_user(request):
	serializer = GetFullUserSerializer(request.user)
	return Response(serializer.data)

class CreateUserView(APIView):
	"""
	Este metodo esta personalizado para la creacion de 
	los usuarios y automaticamente devuelva el token, por lo cual
	no funciona en esta documentacion
	Usando Curl la peticion debe ser asi:
	"
	curl --request POST \
	  --url http://localhost:8000/api/users/create \
	  --header 'content-type: application/json' \
	  --data '{"user":{"username":"namecurl1","password":"asdasdasd","first_name":"curl","last_name":"demo1"}}' 
	 "
	 con eso se crean usuarios sin privilegios de admin y devuelve el token del usuario creado

	"""
	permission_classes = (permissions.AllowAny, )
	def post(self,request):
		user = request.data.get('user')
		#print(request.data)
		#username=str(user['username'])
		#print(username)
		#passs=str(user['password'])
		if not user:
			return Response({'response' : 'error', 'message' : 'No data found'})
		serializer = UserSerializerWithToken(data = user)
		#uss = User.objects.(
        #    username = user['username']
        #)
		if serializer.is_valid():
			saved_user = serializer.save()
			#print(username)
			#authenticate(username=username, password=passs)
			#payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			#encode_handler = api_settings.JWT_ENCODE_HANDLER		
			#payload = payload_handler(uss)
			#token = encode_handler(payload)

				
		else:
			return Response({"response" : "error", "message" : serializer.errors})
		#login(request,user)
		return Response({"response" : "success", "message" : "user created succesfully"})
		#return Response({"response" : "success",'token': token})

