from django.urls import path
from . import views

urlpatterns = [
    path('business/profile/lsit/', views.BusinessProfileListAPIView.as_view()),
    path('business/profile/', views.BusinessProfileAPIView.as_view()),
    path('payment-method/',views.PaymentMethodAPIView.as_view()),

]