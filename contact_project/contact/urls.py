from django.urls import path
from .views import ContactView, MessageListView

urlpatterns = [
    path('contact/', ContactView.as_view()),
    path('messages/', MessageListView.as_view()),
]
