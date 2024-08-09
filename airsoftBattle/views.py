from django.utils import timezone
from datetime import timedelta
import random
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from airsoftBattle.forms import PartidaForm, RegistroUsuarioForm
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Count

from airsoftBattle.models import Material, Partida, Reserva, Usuario

# Create your views here.

#region Home

def home(request):
    partidas = Partida.objects.filter(estado='abierta')

    return render(request,'airsoftBattle/home.html', {'partidas':partidas})

#endregion

#region CRUD partida
def listadoPartidas(request):
    partidas = Partida.objects.all().order_by('-fechaInicio', '-horaInicio')
    return render(request, 'airsoftBattle/partida/listado.html', {'partidas': partidas})

class CrearPartida(View):
    templateList = 'airsoftBattle/partida/crearPartida.html'

    def get (self,request):
        form = PartidaForm()
        return render(request, self.templateList, {'form':form})
    
    def post (self,request):
        form = PartidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listadoPartidas')
        return render(request, self.templateList, {'form':form})

def detallePartida(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    return render(request, 'airsoftBattle/partida/detalle.html', {'partida': partida})


class EditarPartida(UpdateView):
    model = Partida
    fields = '__all__'
    template_name = 'airsoftBattle/partida/editar.html'
    success_url = reverse_lazy('listadoPartidas')



class EliminarPartida(DeleteView):
    model = Partida
    template_name = "airsoftBattle/partida/eliminar.html"
    success_url = reverse_lazy ('listadoPartidas')

#endregion

#region registar usuario
def registrarUsuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrado con éxito')
            return redirect('home')
        messages.error(request, 'Error en el registro.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registrar.html', {'form':form})
#endregion

#region participar en partida y alquilar material

class ParticiparEnPartida(View):
    templateList = 'airsoftBattle/partida/participarEnPartida.html'

    def get (self, request, pk):
        partida = get_object_or_404(Partida, pk=pk)
        return render(request,self.templateList,{'partida':partida})

    def post (self,request,pk):

        partida = get_object_or_404(Partida, pk=pk)
        rol_seleccionado = request.POST.get('rol')
        alquilarMaterial = request.POST.get('alquilarMaterial')

        if rol_seleccionado is None:
            messages.error(request,'No ha seleccionado bando')
            return render(request, self.templateList, {'partida': partida})
        
        if partida.rolMilitar.filter(id__contains=request.user.id).exists() or partida.rolPMC.filter(id__contains=request.user.id).exists():
            messages.error(request, 'Ya estás apuntado en esta partida.')
            return render(request, self.templateList, {'partida': partida})

        if (partida.rolMilitar.count() + partida.rolPMC.count()) < partida.totalJugadores:
            if  rol_seleccionado == 'rolMilitar':
                partida.rolMilitar.add(request.user)
            else:
                partida.rolPMC.add(request.user)
        else:
            messages.error(request, 'Se ha alcanzado el numero máximo de jugadores en esta partida. No puede apuntarse.')
            return render(request, self.templateList, {'partida': partida})
        partida.save()

        if alquilarMaterial == 'on':
            return redirect ('alquilarMaterial', pk=pk)

        return redirect ('detallePartida', pk=pk)

class ListadoMaterial (ListView):
    model = Material
    template_name = "airsoftBattle/material/listadoMaterial.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replicas'] = Material.objects.filter(tipo='replica')
        context['protecciones'] = Material.objects.filter(tipo='proteccion')
        return context

class AlquilarMaterial (View):
    templateList = 'airsoftBattle/material/alquilar.html'

    def get (self, request, pk):
        replicas = Material.objects.filter(tipo = 'replica')
        protecciones = Material.objects.filter(tipo = 'proteccion')
        return render(request,self.templateList,{'replicas': replicas, 'protecciones': protecciones})
    
    def post (self,request, pk):

        replica = None
        proteccion = None

        if request.POST['replica'] :
            replica = get_object_or_404(Material, pk=request.POST['replica'])
            replica.estado = 'reservada'
            replica.save()

        if request.POST['proteccion']:
            proteccion = get_object_or_404(Material, pk=request.POST['proteccion'])
            proteccion.estado = 'reservada'
            proteccion.save()

        partida = get_object_or_404(Partida, pk=pk)
        partida.save()

        Reserva.objects.create(
            usuario = request.user,
            replica = replica,
            proteccion = proteccion,
            partida = partida,
        )

        return redirect ('detallePartida', pk=pk)

def reorganizarEquipos(request,pk):
    DIFERENCIAMAXIMA1 = -1 #para contemplar que la resta pueda salir negativa
    DIFERENCIAMAXIMA2 = 1
    
    partida = get_object_or_404(Partida, pk=pk)
    diaAnteriorPartida= partida.fechaInicio - timedelta(days=1)

    if diaAnteriorPartida == timezone.now().date():
        diferenciaEquipos = partida.rolMilitar.count() - partida.rolPMC.count()

        if diferenciaEquipos not in range(DIFERENCIAMAXIMA1, DIFERENCIAMAXIMA2):
            todosLosJugadores = []

            for jugador in partida.rolMilitar.all():
                todosLosJugadores.append(jugador)
            for jugador in partida.rolPMC.all():
                todosLosJugadores.append(jugador)

            partida.rolMilitar.clear()
            partida.rolPMC.clear()

            alternarEquipo = True
            while ( todosLosJugadores ):
                indiceRandom = random.randrange(0, len(todosLosJugadores))
                if alternarEquipo:
                    partida.rolMilitar.add(todosLosJugadores[indiceRandom])
                    del todosLosJugadores[indiceRandom]
                else:
                    partida.rolPMC.add(todosLosJugadores[indiceRandom])
                    del todosLosJugadores[indiceRandom]
                    
                alternarEquipo = not alternarEquipo
        messages.info(request,'Equipos equilibrados en número de jugadores')
        return render(request, 'airsoftBattle/partida/detalle.html', {'partida': partida})
    
    messages.info(request,'Esto solo puede hacerse el dia antes de la partida.')
    return render(request, 'airsoftBattle/partida/detalle.html', {'partida': partida})

#endregion

#region galeria
def galeriaImagenes(request):

    imagenes = []
    
    for partida in Partida.objects.all():
        if partida.galeriaFotos:
            imagenes.append(partida.galeriaFotos)

    paginator = Paginator(imagenes, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'airsoftBattle/galeria/galeriaImagenes.html', { "page_obj": page_obj})
#endregion

#region informe

class InformeAsistencia(ListView):
    model=Partida
    template_name = 'airsoftBattle/informes/informeAsistencia.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #[:3] se indica que solo nos devuelva tres
        mayorAsistencias = Usuario.objects.annotate(totalAsistencias=Count('militares') + Count('pmcs')).order_by('-totalAsistencias')[:3]
        context['mayorAsistencias'] = mayorAsistencias
        menosAsistencias = Usuario.objects.annotate(totalAsistencias=Count('militares') + Count('pmcs')).order_by('totalAsistencias')[:3]
        context['menosAsistencias'] = menosAsistencias
        return context

#endregion
