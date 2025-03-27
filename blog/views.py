from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.authtoken.models import Token
from .models import Post, Like
from django.core import serializers
import json

# Create User
class CreateUserView(generics.CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

#User Login View
class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            print(user)

            print(user.password)
            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response(status=200, data = {"msg" :  "Login Successfully.", "token": str(token)})
            
            return Response(status=400, data = {"msg": 'User creadentials are invalid'})
        
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg": 'Internal Server Error!', 'error': str(e)})
    
#Update User
class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

#Delete User
class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

#Retrive User
class GetUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    

#Create Post View
class CreateRetrievePostView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            if request.user.is_authenticated:
                serializer = PostSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=201, data = {"msg" :  "Post Created.", "post": serializer.data})
                else:
                    return Response(status=400, data = {"msg" :  "Bad Data.", "error": serializer.error})
            else:
                return Response(status=400, data = {"msg" : "UnAuthorized User."})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        
    def get(self, request):
        try:
            if request.user.is_authenticated:
                posts = Post.objects.filter(is_public=True) | Post.objects.filter(user=request.user)
            else:
                posts = Post.objects.filter(is_public=True)
            print(type(posts), posts)
            posts = json.loads(serializers.serialize('json', posts))
            
            return Response(status=200, data = {"msg" :  "Post's Fetched.", "posts" : posts})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        

class IsOwnerUser(BasePermission):   
    def has_object_permission(self, request, view, obj):
        print("user : ", request.user, obj)
        return obj.user == request.user


class RetrieveUpdateDeletePostView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerUser]

    def get(self, request, id):
        try:
            post = Post.objects.filter(id=id)
            if post :
                self.check_object_permissions(request, post.first())
                post = json.loads(serializers.serialize('json', post))
                return Response(status=200, data = {"msg" :  "Post's Fetched.", "posts" : post})
            return Response(status=400, data = {"msg" :  "No Post Found."})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        
    def put(self, request, id):
        try:
            post = Post.objects.get(id=id)
            if post :
                self.check_object_permissions(request, post)
                serializer = PostSerializer(instance=post, data=request.data, context=request)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200, data = {"msg" :  "Blog post updated."})
                else:
                    return Response(status=400, data = {"msg" :  "Bad Data.", "error": serializer.errors})
            return Response(status=400, data = {"msg" :  "No Post Found."})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        
    def delete(self, request, id):
        try:
            post = Post.objects.get(id=id)
            if post :
                self.check_object_permissions(request, post)
                post.delete()
                return Response(status=204, data = {"msg" :  "Post Deleted."})
            return Response(status=400, data = {"msg" :  "No Post Found."})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        

class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, blog_id):
        try:
            post = Post.objects.get(id=blog_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                return Response(status=201, data = {"msg" :  "Post Liked."})
            return Response(status=200, data = {"msg" :  "Post Already Liked."})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        
    def delete(self,request, blog_id):
        try:
            post = Post.objects.get(id=blog_id)
            like = Like.objects.filter(user=request.user, post=post)
            if like:
                like.delete()
                return Response(status=204, data = {"msg" :  "Post Unlike."})
            return Response(status=204, data = {"msg" :  "Post Wasn't Liked."})
        except Exception as e:
            print(str(e))
            return Response(status=500, data = {"msg" :  "Internal Server Error.", "error" : str(e)})
        
        