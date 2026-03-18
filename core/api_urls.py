from rest_framework.routers import DefaultRouter
from .views import (
    VoluntarioViewSet,
    AcaoComunitariaViewSet,
    InscricaoViewSet,
    CampanhaViewSet,
)

router = DefaultRouter()
router.register(r'voluntarios', VoluntarioViewSet)
router.register(r'acoes', AcaoComunitariaViewSet)
router.register(r'inscricoes', InscricaoViewSet)
router.register(r'campanhas', CampanhaViewSet)

urlpatterns = router.urls