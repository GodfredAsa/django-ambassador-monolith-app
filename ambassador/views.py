from rest_framework.views import APIView
import string, random
from .serializers import ProductSerializer, LinksSerializer, UserSerializer
from django_redis import get_redis_connection
from core.models import Product, Link, Order, User
from rest_framework.response import Response
from rest_framework import status
from common.authentication import JwtAuthentication
from rest_framework.permissions import IsAuthenticated


class ProductFrontendApiView(APIView):
    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductBackendApiView(APIView):
    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LinkApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = LinksSerializer(data={
            'user': user.id,
            'code': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
            'products': request.data['products']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatsApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        links = Link.objects.filter(user_id=user.id)
        return Response([self.format_link(link) for link in links], status=status.HTTP_200_OK)

    @staticmethod
    def format_link(link):
        orders = Order.objects.filter(code=link.code, complete=1)
        return {
            'code': link.code,
            'count': len(orders),
            'revenue': sum(order.ambassador_revenue for order in orders)
        }


class RankingApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ambassadors = User.objects.filter(is_ambassador=True)
        ret_json = list({
            "name": a.name,
            "revenue": a.revenue
        } for a in ambassadors)
        ret_json.sort(key=lambda a: a['revenue'], reverse=True)
        return Response(ret_json, status=status.HTTP_200_OK)

