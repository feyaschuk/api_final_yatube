from django.contrib.auth.models import User
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


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
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True, required=False)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Follow

    def create(self, validated_data):
        following = validated_data.pop('following')
        user = self.context['request'].user
        if user == following:
            raise serializers.ValidationError("You can't sign up to yourself")
        elif Follow.objects.filter(following=following,
                                   user=user).exists():
            raise serializers.ValidationError('You already signed up')        
        else:
            follow = Follow.objects.create(following=following, user=user)
            return follow
   

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
