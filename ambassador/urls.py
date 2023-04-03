from django.urls import path, include
from .views import ProductBackendApiView, ProductFrontendApiView, LinkApiView, StatsApiView, RankingApiView


urlpatterns = [
    path('', include('common.urls')),
    path('products.frontend', ProductFrontendApiView.as_view()),
    path('products.backend', ProductBackendApiView.as_view()),
    path('links', LinkApiView.as_view()),
    path('stats', StatsApiView.as_view()),
    path('rankings', RankingApiView.as_view()),

]