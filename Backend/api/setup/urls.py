from pathlib import os

from django.contrib import admin
from django.urls import path
from django.conf import settings

from rest_framework import permissions, routers

from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from dotenv import load_dotenv

from games.views import GameListView, GameSingleView
from payment.views import PriceCheckerViewSet, PaymentViewSet
from product_cart.views import ProductsCartViewset
from user.views import UserView

load_dotenv()


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
api_router = routers.DefaultRouter()

urlpatterns = [
    path(os.environ.get('ADMIN_URL'), admin.site.urls),
    path('user/', UserView.as_view(), name='user_view'),
    path('cart/', ProductsCartViewset.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='products_cart_view'),
    path('games/', GameListView.as_view(), name='games_view'),
    path('games/<int:pk>/', GameSingleView.as_view(), name='game_view'),
    path('price-check/', PriceCheckerViewSet.as_view({'get': 'list'}), name='price_check_view'),
    path('payment/', PaymentViewSet.as_view({'post': 'create'}), name='payment_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


docs_urls = (
    path('swagger_json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
)


urlpatterns += docs_urls
