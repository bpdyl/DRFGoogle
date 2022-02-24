from functools import partial
from multiprocessing import AuthenticationError
from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.decorators import login_required
from Accounts.serializers import PostSerializer, UserProfileUpdate
from rest_framework.decorators import action
from .models import CustomUser, Post
import requests
# Create your views here.

# @login_required
def home(request,*args,**kwargs):
    current_user = request.user
    if current_user.is_authenticated:
        if not current_user.profile_completed:
            return redirect('profile-fill')
    return render(request,'profile.html')

@login_required
def profile_update(request):
    print("First request",request.GET)
    p = {'username':request.user.username}
    r = requests.get('http://localhost:8000/update_user_profile',params = p)
    context = {}
    context['u'] = r.json() 
    print("fill data",r.json())
    return render(request,'profile_fill.html',context)

class MyView(generics.ListAPIView):
    """
    This View is a proof that the access token generated with drf-social-oauth2 works.
    Try firing a request to http:127.0.0.1:8000/read with and without the token.
    """
    def get(self, request, *args, **kwargs):

        response = {
            'message': 'token works.',
            'user':self.request.user.username,
        }
        return Response(response, status=200)

class UpdateProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileUpdate
    # permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        current_user = self.request.user
        return CustomUser.objects.filter(username = user.username)

    def list(self,request,*args,**kwargs):
        user = request.user
        print("i am user",user)
        param = request.GET.get('username')
        print("I am request.user",param)
        current_user = CustomUser.objects.filter(username = param)
        print("this is current  user",current_user)
        serializer = UserProfileUpdate(current_user,many=True)
        print("This is data",serializer.data)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        response = super(UpdateProfileView, self).create(request, *args, **kwargs)
        print("this is response",response)
        return HttpResponseRedirect(redirect_to='/')  
    def update(self,request,*args,**kwargs):
        user_obj = self.request.user
        print("user obj",user_obj)
        data = request.data
        print("unformatted data",data)
        # user_obj.first_name = data['first_name']
        # user_obj.last_name = data['last_name']
        # user_obj.addresss = data['address']
        # user_obj.phone_number = data['phone_number']
        # user_obj.gender = data['gender']
        # user_obj.interest = data['interest']
        # user_obj.profile_image = data['profile_image']
        # user_obj.profile_completed = True
        # user_obj.save()
        serializer = UserProfileUpdate(instance = user_obj,data=request.data,partial = True)
        if data['profile_image'] == '':
            print("no image coming")
            if user_obj.profile_image:
                photo = user_obj.profile_image
                print("existing photo",photo)
            else:
                DEFAULT = 'user_photos/nouser.jpg'
                photo = DEFAULT
                print("no image found so setting default",photo)

        else:
            photo = data['profile_image']
            print("naya aako photo",photo)
        if serializer.is_valid():
            serializer.save(profile_completed = True,profile_image = photo)
        else:
            print("invalid data")
            print(serializer.errors)
        return HttpResponseRedirect(redirect_to='/profile')


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        post = Post.objects.all()
        current_user = self.request.user
        response = {
            'post':post,
            'current_user':self.request.user,
        }
        return post
    def create(self, request, *args, **kwargs):
        response = super(PostView, self).create(request, *args, **kwargs)
        print("this is response",response)
        return HttpResponseRedirect(redirect_to='/profile')    
    def perform_create(self, serializer):
        print("this is request user",self.request.user)
        serializer.save(author = self.request.user)


    # def get(self,request,*args,**kwargs):
    #     queryset = Post.objects.all()
    #     serializer_class = PostSerializer
    #     response = {
    #         'posts': serializer_class.data
    #     }
    #     return Response(response)
    # def post(self,request,*args,**kwargs):
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         question = serializer.save()
    #         serializer = PostSerializer(question)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def my_profile(request,*args,**kwargs):
    current_user=  request.user
    context = {}
    context['user'] = current_user
    return render(request,'profile.html',context)