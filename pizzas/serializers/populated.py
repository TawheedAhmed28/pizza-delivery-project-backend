from rest_framework import serializers
from .common import PizzaSerializer, ToppingSerializer

class PopulatedPizzaSerializer(PizzaSerializer):
    toppings = ToppingSerializer(many=True)