from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('livebusdata/', include('livebusdata.urls')),  # Include livebusdata routes
    path('', RedirectView.as_view(url='/livebusdata/', permanent=True)),

]
