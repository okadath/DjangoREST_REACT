esto lo hice con al version de django que manejas

```
django==2.1
djangorestframework==3.8.2
django-cors-headers==2.2.0
djangorestframework-jwt
```
Por que en AWS las instancias o son 3.4 o 3.6
por lo cual no usan tu version de python
y preferi usar una superior para evitar errores de dependencias y desarrollo

```bash
django-admin startproject library_project
cd library_project
python manage.py  migrate
```
Las apps son areas discretas de funcionalidad, aqui hay intercomunicacion entre ellas, en Elixir hay que generar una umbrella :'v

Agregar la nueva app a `installed_apps` en `settings.py`, nunca olvidar dejar una coma al final para seguir agregando elementos al recurso en automatico
migrar

```bash
python manage.py startapp todos
python manage.py  migrate
python manage.py runserver

```
![iniciando server](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/django.png)
<!-- 
## Cap 2 Django tradicional
agregar a books.models
```python
# Create your models here.
class Book(models.Model):
	title=models.CharField(max_length=250)
	subtitle=models.CharField(max_length=250)
	author=models.CharField(max_length=100)
	isbn=models.CharField(max_length=13)

	def __str__(self):
		return self.title


```
python manage.py  makemigrations books
python manage.py  migrate

python manage.py  createsuperuser

agregar a books/admin.py

```python
from .models import Book

# Register your models here.
admin.site.register(Book)
```
en books/views
 -->

## Cap 3 REST


```python 
from django.db import models

# Create your models here.
class Todo(models.Model):
	title=models.CharField(max_length=200)
	body=models.TextField()

	def __str__(self):
		return self.title
```

```bash
python manage.py  makemigrations todos
python manage.py  migrate

python manage.py  createsuperuser
```

CORS permite el acceso a la api desde otros lugares 
usar un middleware el djangocors
y actualizar el settings.py:
```python
INSTALLED_APPS = [
	...
  'todos',
  'rest_framework',
  'corsheaders',
]

REST_FRAMEWORK={
  'DEFAULT_PERMISSION_CLASSES':[
  'rest_framework.permissions.AllowAny',
  ]
}
MIDDLEWARE = [
	...
  'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
]
CORS_ALLOW_CREDENTIALS = True
```
python manage.py  makemigrations todos(en plural)
python manage.py  migrate


```python
from django.contrib import admin
from .models import Todo
admin.site.register(Todo)
```
crear superusuario y correr, agregar 3 todos

hay 3 archivos 


+ URLS:
 En todo_project/urls.py agregar en el array(nunca pinches putas perras olvidar que se debe agregar el include en versiones superiores al 2.0 para el manejo de urls,cuando hay errores a veces no hay autorefresh en django, hay que cerrar el server con Ctrl+C en consola, el cambio de sintaxis entre versiones me causo dolores de cabeza por dias la primera vez que toque django!!!!!!! >:v ):
![error en URL](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/error.png)

 ya corregido:
```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todos.urls')),
]

```


Crear en `todos/urls.py`:
```python
from django.urls import path

from .views import ListTodo, DetailTodo

urlpatterns=[
path('',ListTodo.as_view()),
path('<int:pk>/',DetailTodo.as_view()),
]
```
El list nos dara todos
int pk es para dar solo un item

+ todos/serializers.py:
Convierten los datos crudos en un JSON
crear todos/serializers.py

```python
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
	class Meta:
		model=Todo
		fields=('id','title','body',)
```
Es similar a los modelos de clases de django, id es generado automaticamente

+ todos/views.py:

creamos las clases que usaran las urls

```python
#from django.shortcuts import render

from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer

class ListTodo(generics.ListAPIView):
	queryset=Todo.objects.all()
	serializer_class=TodoSerializer

class DetailTodo(generics.RetriveAPIView):
	queryset=Todo.objects.all()
	serializer_class=TodoSerializer
```

Accediendo a la URL
+ Para ver todos los items:
![lista](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/APIlist.png)
+ Para verlos en formato JSON:
![json](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/APIJSON.png)
+ Para ver un solo item:
![item](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/APIitem.png)
## Cap 4 REACT

yo uso yarn, npm igual sirve
```bash
sudo npm install -g create-react-app
create-react-app frontend
cd frontend
npm start
```
![react](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/createreact.png)

y editamos el src/App.js:
```javascript
import React, { Component } from 'react';
const list=[
{"id":1,
"title":"1rt todo",
"description":"asdasdasd"
},
{"id":2,
"title":"2nd todo",
"description":"qweqweqwe"
},
]
class App extends Component{
  constructor(props) {
    super(props);
  
    this.state = {list};
  }
  render(){
    return{
      <div>
      {
        this.state.list.map(item=>(
          <div key={item.id}>
          <h1>{item.title}</h1>
          </div>
          ))}
        </div>
    };
  }
}
export default App;
```
![react estatico](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/static.png)

ya con el estatico siguiendo el workflow de React creamos los datos dinamicos
instalamos axios para manejar la conexion:
```npm install axios```

 y colvemos editar el App.js:
```javascript
import React, { Component } from 'react';
import axios from 'axios';
class App extends Component{
  state={
    todos:[]
  };
  componentDidMount(){
    this.getTodos();
  }
  getTodos(){
    axios
    .get('http://127.0.0.1:8000/api/')
    .then(res=>{
      this.setState({todos:res.data});
    })
    .catch(err=>{
      console.log(err);
    });
  }
  render(){
    return(
      <div>
      {
        this.state.todos.map(item=>(
          <div key={item.id}>
          <h1>{item.title}</h1>
          <span>{item.body}</span>
          </div>
          ))}
        </div>
    );
  }
}
export default App;

```
![react dinamico](https://raw.githubusercontent.com/okadath/DjangoREST/master/pics/dinamic.png)

y corriendo el server de django como el server de react obtenemos:
```bash
npm start
python manage.py runserver
```

voy a seguir con el libro por que aqui solo es usando GET, falta la autenticacion y POST

# Caps 5-6

Ciclo de creacion:

```python
models  ->
		views->urls
serializer->
```
models:
```py
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```
serializer:
```py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at',)
        model = Post
```
views(cambiarle el nombre a APIviews para evitar errores):

```py
from rest_framework import generics

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

urls: 
```py
from django.urls import path

from .views import PostList, PostDetail

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view()),
    path('', PostList.as_view()),
]
```
en el urls principal:
```py
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
```

## Authorization:
agregar al `urls.py` principal:
```python
path('api-auth/', include('rest_framework.urls')),
```
y eso usara el login por default de DRF

en el `settings.py` agregamos los permisos:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

y en las vistas ponemos

```python
from rest_framework import permissions

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    ...
```
para limitar los permisos:

+ AllowAny
+ IsAuthenticated
+ IsAdminUser
+ IsAuthenticatedOrReadOnly

Si se ponen en el `settings.py`  entonces se aplican a todas las vistas

### Custom permissions

creamos un archivo `posts/permissions.py`:
```python
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of a post
        return obj.author == request.user
```

y lo heredamos en el `views.py`:
```python
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
   ```

### Authentication:

el pinche libro usa el manejo de tokens por default de DRF, nosotros usaremos JWT

### Routes/endpoints
 para evitar la repeticion de codigo 

# JWT

instalar y agregar al settings:
```
 pipenv install djangorestframework-jwt django-rest-auth
```

agregamos en el `setings.py` los permisos, tendremos todo solo para autenticados excepto el sign up
```py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

...

CORS_ALLOW_CREDENTIALS = True
```
detalle en cors:
You can chose to either white list all (Definitely not recommended), or white-list just your react host, localhost with port 3000 being the default config.

## .................................
modificamos el admin y el modelo de profiles, son relativamente independientes del login asi que es mas facil manejarlos
## Authentication:

el pinche libro usa el manejo de tokens por default de DRF, nosotros usaremos JWT

primero las rutas quedaran asi:
```py
admin/

#datos
api/

#autenticacion
auth/token-auth/#obtiene el token a partir de nombre:password
auth/login/ [name='rest_login']
auth/logout/ [name='rest_logout']
auth/#login/logout DRF podemos no usarlo, es necesario para Swagger

#documentaciones
docs/
schema/#documentacion nativa de DRF, opcional
swagger_docs/
```

a partir del modelo creamos los serializers en `serilizers.py` para el manejo de la info, creamos un serializer personalizado 
que cree el token al vuelo
```py
from rest_framework import serializers
from .models import Post,Profile
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at',)
        model = Post

class GetFullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','is_superuser','first_name', 'last_name')

#serializer de creacion de usuario POST
class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    def get_token(self, object):
        #obtiene el token al vuelo
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(object)
        token = jwt_encode_handler(payload)
        return token
    def create(self, validated_data):
        #crear usuario, los datos se le pasan desde las vistas 
        #con UserSerializerWithToken(data = user)
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'first_name',
        'last_name')      

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user.username', 'bio')

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        return instance 

```
luego en su `views.py` creamos la vista de esos serializers, en la mayoria son comunes y corrientes excepto
en el modelo de usuarios:
```py
from rest_framework import generics,viewsets, generics, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view#para el decorador
from django.contrib.auth.models import User
from .serializers import UserSerializerWithToken, GetFullUserSerializer
from rest_framework.response import Response

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
    if not user:
      return Response({'response' : 'error', 'message' : 'No data found'})
    serializer = UserSerializerWithToken(data = user)
    if serializer.is_valid():
      saved_user = serializer.save()
    else:
      return Response({"response" : "error", "message" : serializer.errors})
    return Response({"response" : "success", "message" : "user created succesfully"})

```

en el `app/urls.py` agregamos las rutas, las de los items podrian ser creadas con routes, aun no lo checo
las rutas de los users son personalizadas por que no estoy borrando usuarios, ni editando su info o su contraseña, creo que eso lo hare despues, aqui no importa mucho...creo
```py
from django.urls import path
from .views import *
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view()),
    path('', PostList.as_view()),
    path('users/current_user/', get_current_user),
    path('users/', CreateUserView.as_view()  ),
    path('users/list', GetAllUserAndProfiles.as_view()),
    path('auth-jwt-refresh/', refresh_jwt_token),
]
```
tambien crearemos una funcion para la devolucion del token por default en cualquier operacion no definida pero bien creada, creamos un archivo llamado `app/utils.py`:
```py
from todos.serializers import GetFullUserSerializer

def custom_jwt_response_handler(token, user=None, request=None):
    return {
        'token' : token,
        'user' : GetFullUserSerializer(user, context={'request' : request}).data
    }
    ```

y este se agrega al `settings.py` asi como configuraciones para manejar las cabeceras y el tiempo de duracion del token:
```py
...
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER' :   'todos.utils.custom_jwt_response_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=60*24*365*3),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
```

ademas de eso agregamos otras lineas:
```py
import os,datetime

ALLOWED_HOSTS = [*]
# Application definition

INSTALLED_APPS = [
...
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken', # Add this line
    'rest_auth',
]


REST_USE_JWT = True

```
despues de eso solo agregamos las rutas a `urls.py` principal:
```py
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_auth.views import   LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todos.urls')),
    path('auth/token-auth/', obtain_jwt_token),#obtiene el token
    # path('auth/', include('rest_auth.urls')),#si la usamos usaremos muchas rutas por default
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),

]


```

si quisieramos usar las vistas del auth las agregamos a alguna view, el detalle es que incluye todas las vistas(reset de contraseñas y su validacion) :
```py
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
...
    path('auth/', include('rest_auth.urls')),
]
```


## Schemas y documentacion:
instalar
```
pipenv install coreapi pyyaml django-rest-swagger
```
```py
INSTALLED_APPS = [
    ...
    'rest_auth',
    'coreapi',
    'rest-framework-swagger',
    ]
#a veces truena sin el staticfiles, asi que hay que hacer collectstatics
STATIC_URL = '/static/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
```
y agregamos a las `urls.py`:
```py
from django.contrib import admin
from django.urls import path, include
from rest_auth.views import   LoginView, LogoutView
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
Title="API_v0.01"
schema_view=get_schema_view(title=Title)
swagger_view=get_swagger_view(title=Title)

urlpatterns = [
    ...
    #la linea de abajo es para que no truene swagger, pero no se usan 
    #es por un error en el paquete, si quitamos swagger podemos quitar esta ruta
    #si la sobreescribimos con auth internamente hace dos peticiones
    path('auth/', include('rest_framework.urls',  namespace='rest_framework')),
    path('docs/',include_docs_urls(title='API Digital Team Edition v0.01')),
    path('schema/',schema_view),
    path('swagger_docs/',swagger_view),
]

```
y ya podremos acceder en esas rutas a la documentacion, los emtodos personalizados no funcionan en ella
entonces eso se deja indicado en la documentacion de las funciones con entrecomillados """

### Bug:
swagger esta muy bugueado, al parecer no lo actualizaron asi que ademas de necesitar una ruta con 
el nombre de `rest_framework`, para sus plantillas necesita una aplicacion llamada `staticsfile`, en el django actual se usa `static`, entonces se debe de quitar se su plantilla .html ubicada en :
`/.local/share/virtualenvs/DjangoREST-FTSYNYzu/lib/python3.6/site-packages/rest_framework_swagger/templates/rest_framework_swagger` (Django indica donde esta ubicada) y quitar ese load de la cabecera



## API:
+ Crear usuarios:
este es el estilo del users/create_new(solo crea Usuarios sin privilegios!!)
```js
{
  "user":{
  "username":"name1",
  "password":"asdasdasd",
  "first_name":"qweqweqwe",
  "last_name":"asdqweasd"
  }
}
```

no se por que no funciona en Postman, debe ser por las cabeceras,funciona bien con curl

al parecer se deben llamar por partes por que el login no devuelve automaticamente un token
se crea el usuario, se busca su token(publico) 


+ Crear un usuario:
```bash
curl --request POST \
      --url http://localhost:8000/api/users/ \
      --header 'content-type: application/json' \
      --data '{"user":{"username":"namecurl1","password":"asdasdasd","first_name":"curl","last_name":"demo1"}'

```

+ Obtiener el token del usuario actual y debes almacenarlo en tu frontend
```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eX...AiOiJK " -X GET  http://127.0.0.1:8000/api/users/current_user/
```
+ Logearse y devolver el token al autenticarse
```bash
curl --request POST \
      --url http://localhost:8000/auth/login/ \
      --header 'content-type: application/json' \
      --data '{"username": "name1", "password": "asdasdasd"}'
```
```bash
curl --request POST \
      --url http://localhost:8000/auth/token-auth/ \
      --header 'content-type: application/json' \
      --data '{"username": "name1", "password": "asdasdasd"}'
```
```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6Im5hbWUxIiwiZXhwIjoxNjA3Mzk3MDU3LCJlbWFpbCI6IiJ9.ifzjs7FKoH1axtxjzY22cwlPsowXE5QJjEW6cRdgcuw" -X GET  http://127.0.0.1:8000/api/
```



documentacion https://github.com/keshavvinayak01/django-api-oauth https://medium.com/swlh/django-rest-framework-with-react-jwt-authentication-part-1-a24b24fa83cd
 https://medium.com/python-pandemonium/json-web-token-based-authentication-in-django-b6dcfa42a332

## ToDo:
+ editar y eliminar usuarios(solo por el mismo user)
+ editar, eliminar y validar contraseñas sin y/o con emails en el `rest_auth`
+ agregar correctamente a Profiles en la API
+ validar que solo se este logueado en un sitio(aqui no se necesita, pero podria necesitarse)
+ crear viewsets y/o routes para la lectura automatica de los modelos de la api(depende de que me digan,
por que no crearemos ni editaremos o eliminaremos archivos mas que desde un admin, asi que todo seran GETs menos el profile y quiza las licencias)
+ usar un buen frontend para las peticiones
+ ver si se puede integrar con channels o algo asi :v
+ definir correctamente los atributos y/o validaciones de las clases a usar en la API



curl --request POST       --url http://localhost:8000/api/users/new       --header 'content-type: application/json'       --data '{"user":{"username":"namecurl3","password":"asdasdasd","first_name":"curl","last_name":"demo1"}}'

curl -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eX...AiOiJK " -X GET  http://127.0.0.1:8000/api/users/current_user/


si es posible crear usuarios al vuelo entonces tal vez toda la pendejada del serializer sea innesesaria

por el momento asi commiteo, no hay login automatico con el sign in pero lo demas funciona

iniciare a modificar los modelos



