from rest_framework.views import APIView
from core.models import User, Product, Link, Order, OrderItems
from common.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated
from common.authentication import JwtAuthentication
from .serializers import ProductSerializer, LinkSerializer, OrderSerializer


class AmbassadorApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        serializer = UserSerializer(ambassadors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductGenerateApiView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # if pk is provided returns a single product or return all the products
    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        # self.put(request, pk) requires all fields to be part of the data, and
        # we wish to update only some fields hence using partial update
        return self.partial_update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class LinkApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        links = Link.objects.filter(user_id=pk)
        serializers = LinkSerializer(links, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class OrderApiView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(complete=True)
        serializers = OrderSerializer(orders, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)







