from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from posts.models import Group, Post, Follow
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.core.exceptions import ValidationError

from rest_framework import filters
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
                          )


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
        following = serializer.validated_data["following"] 
        if Follow.objects.filter(user=self.request.user, following=following).exists:
            raise ValidationError('You already signed up') 
        
            
              
        if self.request.user==following:
            raise ValidationError("You can't sign up to yourself") 
              
        serializer.save(user=self.request.user)
    
    

    

    