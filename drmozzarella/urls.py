from django.urls    import path, include

from products.views import MenuView, CategoryView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework import routers, permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dr.Mozzarella", # 타이틀
        default_version='v1', # 버전
        description="Dr.Mozzarella API 문서", # 설명
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hanj.kim.10@gmail.com"),
        license=openapi.License(name=""),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    
    path('events'                       , include('events.urls')),
    path('accounts'                     , include('accounts.urls')),
    path('products'                     , include('products.urls')),
    path('orders'                       , include('orders.urls')),
    path('menus'                        , MenuView.as_view()),
    path("categories/<int:category_id>" , CategoryView.as_view())
]