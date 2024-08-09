from django.urls import path,include
from airsoftBattle import views
from airsoftBattle.views import CrearPartida, EditarPartida, EliminarPartida, InformeAsistencia, ParticiparEnPartida, ListadoMaterial, AlquilarMaterial
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('airsoftBattle', views.home, name='home'),
    path('listadoPartidas', views.listadoPartidas, name='listadoPartidas'),
    path('crearPartida', staff_member_required(CrearPartida.as_view()), name='crearPartida'),
    path('detallePartida/<int:pk>',login_required(views.detallePartida),name='detallePartida'),
    path('editarPartida/<int:pk>',staff_member_required(EditarPartida.as_view()),name='editarPartida'),
    path('eliminarPartida/<int:pk>',staff_member_required(EliminarPartida.as_view()),name='eliminarPartida'),
    path('registrar', views.registrarUsuario, name='registrar'),
    path('participarEnPartida/<int:pk>', login_required(ParticiparEnPartida.as_view()), name='participarEnPartida'),
    path('listadoMaterial', login_required(ListadoMaterial.as_view()), name='listadoMaterial'),
    path('alquilarMaterial/<int:pk>',login_required(AlquilarMaterial.as_view()),name='alquilarMaterial'),  
    path('galeriaImagenes',views.galeriaImagenes,name='galeriaImagenes'),
    path('reorganizarEquipos/<int:pk>',staff_member_required(views.reorganizarEquipos),name='reorganizarEquipos'),  
    path('informeAsistencia', staff_member_required(InformeAsistencia.as_view()), name='informeAsistencia'),
    path('api/v1/', include('api.urls',namespace= 'api')),
]