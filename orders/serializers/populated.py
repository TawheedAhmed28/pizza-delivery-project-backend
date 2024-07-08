from rest_framework import serializers
from .common import OrderSerializer
from pizzas.serializers.populated import PopulatedPizzaSerializer
from jwt_auth.serializers import UserSerializer

class PopulatedOrderSerializer(OrderSerializer):
    pizzas = PopulatedPizzaSerializer(many=True)
    owner = UserSerializer()