from rest_framework import serializers
from airsoftBattle.models import Material, Reserva


class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ReservasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'