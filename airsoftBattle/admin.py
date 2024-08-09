from .models import Usuario, Partida, Galeria, Material, Reserva
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
  model = Usuario
  fieldsets = UserAdmin.fieldsets + (
  (None, {'fields': ('totalPartidas',)}),
  )

add_fieldsets = UserAdmin.add_fieldsets + (
(None, {'fields': ('totalPartidas',)}),
)

# Register your models here.
admin.site.register(Usuario,CustomUserAdmin)
admin.site.register(Partida)
admin.site.register(Galeria)
admin.site.register(Material)
admin.site.register(Reserva)