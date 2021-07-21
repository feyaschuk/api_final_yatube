from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True, required=False)    
    following = serializers.SlugRelatedField(
        slug_field='username', queryset = User.objects.all())
    
    
    class Meta:
        fields = '__all__'
        model = Follow   
  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
