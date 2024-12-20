from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Client, Employee, Product, Order, OrderDetails
from .serializers import ClientSerializer, EmployeeSerializer, ProductSerializer, OrderSerializer, OrderDetailsSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        # Перевірка унікальності email
        if Client.objects.filter(email=serializer.validated_data['email']).exists():
            raise ValueError("A client with this email already exists.")
        serializer.save()

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Перевірка статусу замовлення
        if serializer.validated_data['status'] not in ['Pending', 'Completed', 'Cancelled']:
            raise ValueError("Invalid status. Allowed values are 'Pending', 'Completed', 'Cancelled'.")
        serializer.save()

class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

    def perform_create(self, serializer):
        # Перевірка наявності продукту
        if serializer.validated_data['quantity'] <= 0:
            raise ValueError("Quantity must be greater than zero.")
        serializer.save()

class OrderDetailsList(APIView):
    def get(self, request, format=None):
        order_details = OrderDetails.objects.all()
        serializer = OrderDetailsSerializer(order_details, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailsDetail(APIView):
    def get_object(self, pk):
        try:
            return OrderDetails.objects.get(pk=pk)
        except OrderDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order_detail = self.get_object(pk)
        serializer = OrderDetailsSerializer(order_detail)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order_detail = self.get_object(pk)
        serializer = OrderDetailsSerializer(order_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order_detail = self.get_object(pk)
        order_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
