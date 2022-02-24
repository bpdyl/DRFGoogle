from urllib import request
from rest_framework import serializers
from .models import CustomUser,Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','description',)

class UserProfileUpdate(serializers.ModelSerializer):
    options = (
            ('IT and Networks','IT and Networks'),
            ('UI/UX','UI/UX'),
            ('Web Development','Web Development'),
            ('Devops','Devops'),
        )
    GENDER_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required = True)
    address = serializers.CharField(max_length=100,required = True)
    phone_number = serializers.IntegerField(required = True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES,required = True)
    interest = serializers.ChoiceField(choices=options,required = True)
    profile_image = serializers.ImageField(allow_null = True)
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','address','phone_number','gender','interest','profile_image')

    def get_profile_image_url(self, obj):
        return obj.profile_image.url
class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required= True)
    username = serializers.CharField(required = True)
    password = serializers.CharField(min_length =8, write_only = True)

    class Meta:
        model = CustomUser
        fields = ('email','username','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance