from django.urls import path
from .views import PizzaListView, PizzaDetailView, ToppingListView

urlpatterns = [
    path('', PizzaListView.as_view()),
    path('<int:pk>/', PizzaDetailView.as_view()),
    path('toppings/', ToppingListView.as_view())
]