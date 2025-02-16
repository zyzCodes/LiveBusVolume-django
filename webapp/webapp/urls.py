from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('livebusdata/', include('livebusdata.urls')),  # Include livebusdata routes
=======
    path('livebus/', include('livebus.urls')),
>>>>>>> main
]
