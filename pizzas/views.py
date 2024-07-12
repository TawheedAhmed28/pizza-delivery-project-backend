from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Pizza, Topping
from .serializers.common import PizzaSerializer, ToppingSerializer
from .serializers.populated import PopulatedPizzaSerializer

# Create your views here.

class PizzaListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        
        pizzas = Pizza.objects.all()
        serialized_pizzas = PopulatedPizzaSerializer(pizzas, many=True)
        return Response(serialized_pizzas.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        print(request.data)

        pizzas = Pizza.objects.all()

        for pizza in pizzas:
           
            pizza_toppings = list(pizza.toppings.values_list('id', flat=True))
            if set(pizza_toppings) == set(request.data["toppings"]):

                raise ValidationError({"toppings": ["A pizza with these toppings already exists!"]})

        request.data["owner"] = request.user.id
        pizza_to_add = PizzaSerializer(data=request.data)

        if pizza_to_add.is_valid():

            pizza_to_add.save()
            return Response(pizza_to_add.data, status=status.HTTP_201_CREATED)
        
        return Response(pizza_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

class PizzaDetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_pizza(self, pk): 

        try:

            return Pizza.objects.get(pk=pk)
        
        except Pizza.DoesNotExist:
            
            raise NotFound(detail="The cheese pull doesn't go that far... this pizza doesn't exist!")

    def get(self, _request, pk):

            pizza = self.get_pizza(pk=pk)
            serialized_pizza = PopulatedPizzaSerializer(pizza)
            return Response(serialized_pizza.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        
        pizza_to_edit = self.get_pizza(pk=pk)

        pizzas = Pizza.objects.all()

        for pizza in pizzas:
           
            pizza_toppings = list(pizza.toppings.values_list('id', flat=True))
            if set(pizza_toppings) == set(request.data["toppings"]):

                raise ValidationError({"toppings": ["A pizza with these toppings already exists!"]})

        if pizza_to_edit.owner.id != request.user.id and not (request.user.is_staff or request.user.is_superuser):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        first_owner = pizza_to_edit.owner.id
        request.data["owner"] = first_owner

        updated_pizza = PizzaSerializer(pizza_to_edit, data=request.data)

        if updated_pizza.is_valid():
            
            updated_pizza.save()
            return Response(updated_pizza.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_pizza.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, request, pk):

        if not (request.user.is_staff or request.user.is_superuser):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
       
        pizza_to_delete = self.get_pizza(pk=pk)
        pizza_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ToppingListView(APIView):

    def get(self, _request):

        toppings = Topping.objects.all()
        serialized_toppings = ToppingSerializer(toppings, many=True)
        return Response(serialized_toppings.data, status=status.HTTP_200_OK)
