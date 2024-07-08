from django.db import models
from pizzas.models import Pizza

# Create your models here.

class Order(models.Model):

    # need help with def __str__() here
    # Pizza: [toppings], Pizza: [toppings]

    def __str__(self) -> str:

        return f'Order ID  {self.id}'

    pizzas = models.ManyToManyField(Pizza, related_name="orders")
    notes = models.TextField(max_length=500, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "jwt_auth.User",
        related_name="owners",
        on_delete=models.CASCADE
    )