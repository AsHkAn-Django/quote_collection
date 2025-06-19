from rest_framework import serializers
from .models import Quote, Comment, SubComment, Like



class QuoteSerializer(serializers.ModelSerializer):
    publisher_username = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = ('id', 'body', 'publisher', 'publisher_username', 'author', 'like_numbers')

    def get_publisher_username(self, obj):
        return obj.publisher.username