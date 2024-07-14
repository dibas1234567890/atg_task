from rest_framework import serializers
from django.contrib.auth import get_user_model
from login_system.models import BlogModel, CustomerUserProfile
User = get_user_model()
from rest_framework import serializers
from .models import Category, CustomerUserProfile





class CustomRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    profile_picture = serializers.ImageField(required=False)
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password1 = serializers.CharField(max_length=100, write_only=True)
    password2 = serializers.CharField(max_length=100, write_only=True)
    address_line1 = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    pincode = serializers.CharField(max_length=10)
    user_type = serializers.ChoiceField(choices=[('patient', 'patient'), ('doctor', 'doctor')])

    def validate_email(self, value):
        if CustomerUserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = CustomerUserProfile(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_picture=validated_data.get('profile_picture'),
            username=validated_data['username'],
            email=validated_data['email'],
            address_line1=validated_data['address_line1'],
            city=validated_data['city'],
            state=validated_data['state'],
            pincode=validated_data['pincode'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password1'])  
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CategorySerializer(serializers.Serializer):
    category_name = serializers.CharField()
    category_slug = serializers.SlugField()

    def create(self, validated_data): 
        category_instance = Category.objects.create(category_name = validated_data['category_name'],
        category_slug = validated_data['category_slug'])
        category_instance.save()
        return category_instance


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = '__all__'
