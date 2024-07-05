from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Pizza, Topping
from .serializers.common import PizzaSerializer

# Create your views here.

class PizzaListView(APIView):

    def get(self, _request):
        
        pizzas = Pizza.objects.all()
        serialized_pizzas = PizzaSerializer(pizzas, many=True)
        return Response(serialized_pizzas.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        pizza_to_add = PizzaSerializer(data=request.data)

        if pizza_to_add.is_valid():

            pizza_to_add.save()
            return Response(pizza_to_add.data, status=status.HTTP_201_CREATED)
        
        return Response(pizza_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

class PizzaDetailView(APIView):

    def get_pizza(self, pk): 

        try:

            return Pizza.objects.get(pk=pk)
        
        except Pizza.DoesNotExist:
            
            raise NotFound(detail="The cheese pull doesn't go that far... this pizza doesn't exist!")

    def get(self, _request, pk):

            pizza = self.get_pizza(pk=pk)
            serialized_pizza = PizzaSerializer(pizza)
            return Response(serialized_pizza.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        
        pizza_to_edit = self.get_pizza(pk=pk)
        updated_pizza = PizzaSerializer(pizza_to_edit, data=request.data)

        if updated_pizza.is_valid():
            
            updated_pizza.save()
            return Response(updated_pizza.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_pizza.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, _request, pk):

        pizza_to_delete = self.get_pizza(pk=pk)
        pizza_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)