from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers.common import OrderSerializer
from .serializers.populated import PopulatedOrderSerializer

# Create your views here.

class OrderListView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, _request):
        
        orders = Order.objects.all()
        serialized_orders = OrderSerializer(orders, many=True)
        return Response(serialized_orders.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        request.data["owner"] = request.user.id
        order_to_add = OrderSerializer(data=request.data)

        if order_to_add.is_valid():

            order_to_add.save()
            return Response(order_to_add.data, status=status.HTTP_201_CREATED)
        
        return Response(order_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

class OrderDetailView(APIView):

    permission_classes = (IsAuthenticated,)

    def get_order(self, pk): 

        try:

            return Order.objects.get(pk=pk)
        
        except Order.DoesNotExist:
            
            raise NotFound(detail="The cheese pull doesn't go that far... this order doesn't exist!")

    def get(self, _request, pk):

            order = self.get_order(pk=pk)
            serialized_order = PopulatedOrderSerializer(order)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        
        order_to_edit = self.get_order(pk=pk)

        if order_to_edit.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_order = OrderSerializer(order_to_edit, data=request.data)

        if updated_order.is_valid():
            
            updated_order.save()
            return Response(updated_order.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_order.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, request, pk):

        order_to_delete = self.get_order(pk=pk)

        if order_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)