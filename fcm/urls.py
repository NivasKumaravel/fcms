from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/send_notification/', SendNotificationView.as_view(), name='send-notification'),

]