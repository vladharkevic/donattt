
from django.urls import path
from donate.views import index, generate_invoice, donate

urlpatterns = [
    path('', index, name='index'),
    path('generate_invoice/', generate_invoice, name='generate_invoice'),
    path('donate/', donate, name='donate'),
]
