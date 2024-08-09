from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario (AbstractUser):
  totalPartidas = models.PositiveIntegerField(null= True, blank= True)

  def __str__(self):
    return self.username

class Partida(models.Model):
  STATUS = (
    ('abierta', 'Abierta'),
    ('cerrada', 'Cerrada')
  )

  fechaInicio = models.DateField()
  horaInicio = models.TimeField()
  fechaFin = models.DateField()
  horaFin = models.TimeField()

  totalJugadores = models.PositiveIntegerField(default = 10)
  rolMilitar = models.ManyToManyField(Usuario, related_name='militares', blank=True)
  rolPMC = models.ManyToManyField(Usuario, related_name='pmcs', blank=True)
  estado = models.CharField(max_length=11,choices=STATUS, default='abierta')
  galeriaFotos = models.ImageField(upload_to='partidas/', null= True, blank= True)

  def __str__(self):
    return self.fechaInicio.strftime('%d-%m-%Y')
  
  def formatoHoraInicio (self):
    return self.horaInicio.strftime('%H:%M')
  
  def formatoHoraFin(self):
    return self.horaFin.strftime('%H:%M')


class Galeria(models.Model):
  imagen = models.ImageField(upload_to='partidas', null= True, blank= True)
  partida = models.ForeignKey(Partida, on_delete = models.CASCADE, related_name='imagenes')

class Material(models.Model):
  STATUS1 = (
      ('disponible', 'Disponible'),
      ('reservada', 'Reservada')
  )
  STATUS2 = (
      ('replica', 'Réplica'),
      ('proteccion', 'Protección')
  )

  nombre = models.CharField(max_length=15)
  estado = models.CharField(max_length=20,choices=STATUS1, default='disponible')
  fotoMaterial = models.ImageField(upload_to='material', null= True, blank= True)
  tipo = models.CharField(max_length=20,choices=STATUS2)

  def __str__(self):
    return self.nombre

class Reserva(models.Model):
  usuario = models.ForeignKey('Usuario',on_delete=models.PROTECT)
  replica = models.ForeignKey('Material',on_delete=models.PROTECT, null= True, blank= True,  related_name='replica')
  proteccion = models.ForeignKey('Material',on_delete=models.PROTECT, null= True, blank= True,  related_name='proteccion')
  partida = models.ForeignKey('Partida',on_delete=models.PROTECT)

  def __str__(self):
    return self.usuario.username + " " + self.partida.fechaInicio.strftime('%d-%m-%Y')
  
  class Meta:
    unique_together = ['usuario','partida']