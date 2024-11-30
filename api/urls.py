from django.urls import path
from .views import submit, locations


urlpatterns = [
    path('submit/',submit ,name='submit'),
    path('api/locations/', locations, name='locations')
]