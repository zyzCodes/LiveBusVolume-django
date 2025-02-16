from django.shortcuts import render
from django.http import HttpResponse
from .models import Bus
from rest_framework import generics
from .serializers import BusSerializer
from datetime import datetime
from django.db.models import Avg, Count, Sum

def home(request):
    """View for the main landing page."""
    return render(request, 'livebusdata/index.html')


def hello_world(request):
    return HttpResponse("Hello, World! 🌍 Welcome to LiveBusData")

# buses list view
def bus_list(request):
    """View to filter buses by bus_id, route, and full date-time range."""
    buses = Bus.objects.all().order_by('-timestamp')

    # Get filter parameters from URL
    bus_id = request.GET.get('bus_id')
    route = request.GET.get('route')
    start_date = request.GET.get('start_date')  # Format: "YYYY-MM-DD"
    end_date = request.GET.get('end_date')  # Format: "YYYY-MM-DD"
    start_time = request.GET.get('start_time')  # Format: "HH:MM"
    end_time = request.GET.get('end_time')  # Format: "HH:MM"

    if bus_id:
        buses = buses.filter(bus_id=bus_id)

    if route:
        buses = buses.filter(route=route)

    # Combine date and time for accurate filtering
    if start_date and start_time:
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            buses = buses.filter(timestamp__gte=start_datetime)
        except ValueError:
            pass

    if end_date and end_time:
        try:
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
            buses = buses.filter(timestamp__lte=end_datetime)
        except ValueError:
            pass

    return render(request, 'livebusdata/bus_list.html', {'buses': buses})

def bus_analytics(request):
    """View to display key analytics for bus ridership."""

    # Aggregate analytics
    avg_passengers_per_route = Bus.objects.values('route').annotate(avg_passengers=Avg('passengers'))
    avg_passengers_per_bus = Bus.objects.values('bus_id').annotate(avg_passengers=Avg('passengers'))
    peak_hour = Bus.objects.annotate(hour=Count('timestamp')).values('hour').annotate(total_passengers=Sum('passengers')).order_by('-total_passengers')[:1]
    daily_total_passengers = Bus.objects.annotate(day=Count('timestamp')).values('day').annotate(total_passengers=Sum('passengers'))
    top_routes = Bus.objects.values('route').annotate(total_passengers=Sum('passengers')).order_by('-total_passengers')[:5]

    return render(request, 'livebusdata/bus_analytics.html', {
        'avg_passengers_per_route': avg_passengers_per_route,
        'avg_passengers_per_bus': avg_passengers_per_bus,
        'peak_hour': peak_hour[0] if peak_hour else None,
        'daily_total_passengers': daily_total_passengers,
        'top_routes': top_routes
    })

# GET (list all buses) & POST (create new bus)
class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all().order_by('-timestamp')
    serializer_class = BusSerializer

# GET (single bus), PUT (update), DELETE (remove)
class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
