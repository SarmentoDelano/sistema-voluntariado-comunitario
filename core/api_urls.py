from rest_framework.routers import DefaultRouter
from .views import (
    VoluntarioViewSet,
    AcaoComunitariaViewSet,
    InscricaoViewSet,
    CampanhaViewSet,
)

router = DefaultRouter()
router.register(r'voluntarios', VoluntarioViewSet, basename='voluntarios')
router.register(r'acoes', AcaoComunitariaViewSet, basename='acoes')
router.register(r'inscricoes', InscricaoViewSet, basename='inscricoes')
router.register(r'campanhas', CampanhaViewSet, basename='campanhas')

urlpatterns = router.urls