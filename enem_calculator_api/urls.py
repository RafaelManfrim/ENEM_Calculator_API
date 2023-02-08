from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from enem_calculator_api.core.API.viewsets import AmbitionViewset, SimulationViewset, UserViewset

router = routers.SimpleRouter()
router.register(r'users', UserViewset, basename='User')
router.register(r'ambitions', AmbitionViewset, basename='Ambition')
router.register(r'simulations', SimulationViewset, basename='Simulation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
