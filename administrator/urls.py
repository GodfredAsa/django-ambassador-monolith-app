from django.urls import path, include
from .views import AmbassadorApiView, ProductGenerateApiView, LinkApiView, OrderApiView
urlpatterns = [
    path('', include('common.urls')),
    path('ambassadors', AmbassadorApiView.as_view()),
    path('products', ProductGenerateApiView.as_view()),
    path('products/<str:pk>', ProductGenerateApiView.as_view()),
    path('users/<str:pk>/links', LinkApiView.as_view()),
    path('orders', OrderApiView.as_view()),

]
