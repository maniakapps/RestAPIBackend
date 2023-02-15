from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from api.views import CompanyView
from . import views

urlpatterns = [
    path("companies/", CompanyView.as_view(), name="companies_list"),
    path('companies/<int:id>', CompanyView.as_view(), name="companies_process"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='auth_login'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', views.TestEndpointView, name='test'),
    path('', views.getRoutes)

]
