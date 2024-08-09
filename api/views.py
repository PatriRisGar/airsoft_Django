from .serializers import MaterialSerializers,ReservasSerializers
from rest_framework import viewsets, permissions
from airsoftBattle.models import Material, Reserva

class MaterialViewSet (viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializers
    permission_classes = [permissions.AllowAny]

class ReservasViewSet (viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservasSerializers
    permission_classes = [permissions.IsAdminUser]