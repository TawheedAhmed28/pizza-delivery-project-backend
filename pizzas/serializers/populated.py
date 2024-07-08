from rest_framework import serializers
from .common import PizzaSerializer, ToppingSerializer
from jwt_auth.serializers import UserSerializer

class PopulatedPizzaSerializer(PizzaSerializer):
    toppings = ToppingSerializer(many=True)
    owner = UserSerializer()