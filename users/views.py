from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payment
from users.serializers import PaymentSerializer

# Create your views here.

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter] 

    filterset_fields = ('course', 'lesson', 'payment_method')

    ordering_fields = ('payment_date',)
