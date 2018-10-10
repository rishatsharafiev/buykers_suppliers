from django.urls import path
from .views import TriggerView

urlpatterns = (
    path('trigger/', TriggerView.as_view()),
)
