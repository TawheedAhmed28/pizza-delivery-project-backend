from rest_framework import serializers
from .common import OrderSerializer
from pizzas.serializers.populated import PopulatedPizzaSerializer

class PopulatedOrderSerializer(OrderSerializer):
    pizzas = PopulatedPizzaSerializer(many=True)