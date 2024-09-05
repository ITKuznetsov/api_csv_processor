from django.urls import path
from .views import ProcessCSVView

urlpatterns = [
    path('process-csv/', ProcessCSVView.as_view(), name='process_csv'),
]