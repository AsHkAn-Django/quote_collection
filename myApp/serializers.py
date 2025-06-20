from rest_framework import serializers
from .models import Quote, Comment, SubComment, Like


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ('id', 'user', 'username', 'quote', 'created_at')

    def get_username(self, obj):
        return obj.user.username


class SubCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubComment
        fields = ('id', 'publisher', 'body', 'created_at', 'comment', 'parent_subcomment')
        read_only_fields = ('publisher',)

class CommentSerializer(serializers.ModelSerializer):
    sub_comments = SubCommentSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'publisher', 'body', 'created_at', 'quote', 'sub_comments')
        read_only_fields = ('publisher',)


class QuoteSerializer(serializers.ModelSerializer):
    publisher_username = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    quote_likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = ('id', 'body', 'publisher', 'publisher_username', 'author', 'like_numbers', 'quote_likes', 'comments')
        read_only_fields = ('publisher',)

    def get_publisher_username(self, obj):
        return obj.publisher.username