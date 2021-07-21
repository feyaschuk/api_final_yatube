from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet): 
    permission_classes = [permissions.IsAuthenticated,]   
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__username', 'following__username']
    
    def get_queryset(self):        
        follow = Follow.objects.filter(user=self.request.user)        
        return follow
    
    def perform_create(self, serializer):
        current_following = serializer.validated_data["following"]         
        
        if self.request.user==current_following:
            raise serializers.ValidationError("You can't sign up to yourself") 
        elif Follow.objects.filter(
            following=current_following, user=self.request.user).exists():
            raise serializers.ValidationError('You already signed up')
        else: 
            serializer.save(user=self.request.user)
         
 