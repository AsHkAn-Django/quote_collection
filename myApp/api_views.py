from rest_framework.decorators import action
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Quote, Comment, SubComment, Like
from .serializers import QuoteSerializer, LikeSerializer, CommentSerializer



class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all().order_by('id')
    serializer_class = QuoteSerializer

    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        likes = Like.objects.filter(quote=quote)
        serializer = LikeSerializer(likes, many=True)
        return Response({'likes': serializer.data})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        comments = Comment.objects.filter(quote=quote)
        serializer = CommentSerializer(comments, many=True)
        return Response({'comments': serializer.data})