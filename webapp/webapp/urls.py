from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('livebusdata/', include('livebusdata.urls')),  # Include livebusdata routes
]
