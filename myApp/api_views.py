from rest_framework import viewsets
from .models import Quote, Comment, SubComment, Like
from .serializers import QuoteSerializer



class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    