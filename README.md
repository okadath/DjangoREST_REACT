esto lo hice con al version de django que manejas

```
django==2.1
djangorestframework3.8.2
django-cors-headers==2.2.0
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
![iniciando server](https://raw.githubusercontent.com/okadath/DjangoREST/master/django.png)
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

CORS_ORIGIN_WHITELIST=(
  'localhost:3000/'
  )
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
![error en URL](https://raw.githubusercontent.com/okadath/DjangoREST/master/error.png)

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
![lista](https://raw.githubusercontent.com/okadath/DjangoREST/master/APIlist.png)
+ Para verlos en formato JSON:
![json](https://raw.githubusercontent.com/okadath/DjangoREST/master/APIJSON.png)
+ Para ver un solo item:
![item](https://raw.githubusercontent.com/okadath/DjangoREST/master/APIitem.png)
## Cap 4 REACT

yo uso yarn, npm igual sirve
```bash
sudo npm install -g create-react-app
create-react-app frontend
cd frontend
npm start
```
![react](https://raw.githubusercontent.com/okadath/DjangoREST/master/createreact.png)

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
![react estatico](https://raw.githubusercontent.com/okadath/DjangoREST/master/static.png)

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
![react dinamico](https://raw.githubusercontent.com/okadath/DjangoREST/master/dinamic.png)

y corriendo el server de django como el server de react obtenemos:
```bash
npm start
python manage.py runserver
```

voy a seguir con el libro por que aqui solo es usando GET, falta la autenticacion y POST


