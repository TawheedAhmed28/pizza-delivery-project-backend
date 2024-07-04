from django.db import models

# Create your models here.
class Topping(models.Model):

    def __str__(self) -> str:
        return f'{self.name}'

    name = models.CharField(max_length=20, unique=True)

class Pizza(models.Model):

    def __str__(self) -> str:

        toppings_names = ", ".join([topping.name for topping in self.toppings.all()])
        return f'{toppings_names}'

    toppings = models.ManyToManyField(Topping, related_name="pizzas")
    is_vegetarian = models.BooleanField()
    is_vegan = models.BooleanField()


