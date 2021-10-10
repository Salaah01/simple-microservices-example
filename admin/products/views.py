import random
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from . import models, serializers, producer

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        producer.publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = models.Product.objects.get(pk=pk)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = models.Product.objects.get(pk=pk)
        serializer = serializers.ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        producer.publish('product_updated', serializer.data)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        product = models.Product.objects.get(pk=pk)
        product.delete()
        producer.publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(views.APIView):
    def get(self, _):
        users = models.User.objects.all()
        user = random.choice(users)
        return Response({'id': user.id})
