from django.urls import path
from .views import PizzaListView, PizzaDetailView

urlpatterns = [
    path('', PizzaListView.as_view()),
    path('<int:pk>/', PizzaDetailView.as_view())
]