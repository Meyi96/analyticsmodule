from django.urls import path
from .views import checkAnomalyUmbral

urlpatterns =[
    path('checkanomaly/<int:experiment_id>', checkAnomalyUmbral.as_view(), name='chaeck_anomaly_umbral')
]

