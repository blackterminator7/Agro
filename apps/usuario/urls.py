from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from apps.usuario.views import Login, logoutUsuario
from apps.usuario.views import ListadoUsuario, RegistrarUsuario


app_name='usuario'

urlpatterns=[
	#URL para el menu de inicio
	path('', index),
	path('usuario/index/',login_required(index), name='index'),

	path('accounts/login/',Login.as_view(), name='login'),
	path('logout/',login_required(logoutUsuario), name='logout'),
	
	path('listado_usuarios/', login_required(ListadoUsuario.as_view()), name='listar_usuarios'),
	path('registrar_usuario/', RegistrarUsuario.as_view(), name='registrar_usuario'),
	]