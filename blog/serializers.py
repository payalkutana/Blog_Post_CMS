from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {"password": {'write_only': True}}

        # def create(self, validated_data):
        #     print('validated_data' ,validated_data)
        #     user = User.objects.create(username = validated_data['username'], 
        #                                email = validated_data['email'],
        #                                password = make_password(validated_data['password']))
        #     return user            

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'created_on', 'is_public', 'user']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'timestamp']

        unique_together = ['post', 'user']