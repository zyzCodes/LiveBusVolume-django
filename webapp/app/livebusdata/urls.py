from django.urls import path
from .views import BusListCreateView, BusDetailView, bus_list, bus_analytics, home

urlpatterns = [
    path('', home, name='home'),  # Landing page at /
    path('buses/', BusListCreateView.as_view(), name='bus-list-create'),
    path('analytics/', bus_analytics, name='bus_analytics'),
    path('buses/<int:pk>/', BusDetailView.as_view(), name='bus-detail'),
    path('buseslist/', bus_list, name='bus_list'),
]