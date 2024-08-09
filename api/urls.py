from rest_framework import routers
from .views import MaterialViewSet,ReservasViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register('material',MaterialViewSet,'material_api')
router.register('reservas',ReservasViewSet,'reservas_api')
urlpatterns = router.urls