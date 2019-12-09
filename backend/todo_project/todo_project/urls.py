"""todo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('admin/', admin.site.urls),
    path('api/', include('todos.urls')),
    path('auth/token-auth/', obtain_jwt_token),
    # path('auth/', include('rest_auth.urls')),
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),
    #la linea de abajo es para que no truene swagger, pero no se usan 
    #es por un error en el paquete, si quitamos swagger podemos quitar esta ruta
    #si la sobreescribimos con auth internamente hace dos peticiones
    path('auth/', include('rest_framework.urls',  namespace='rest_framework')),
    path('docs/',include_docs_urls(title='API Digital Team Edition v0.01')),
    path('schema/',schema_view),
    path('swagger_docs/',swagger_view),
]




