from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication 
from rest_framework.authtoken.models import Token
from login_system.models import Category, CustomerUserProfile
from login_system.serializers import BlogSerializer, CategorySerializer, CustomLoginSerializer, CustomRegisterSerializer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie


class CustomRegisterView(APIView):
    def post(self, request):
        print(request.data['password1'])
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
           
            
            return Response({'message': 'Successfully Registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "token": str(refresh.access_token),
            })
        return Response({"detail": "Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)

class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        display_object = CustomerUserProfile.objects.get(user=user)
        context = {
            'id': display_object.id,
            'username': display_object.user.username,
            'email': display_object.user.email,
            'city': display_object.city
        }
        return Response(context, status=status.HTTP_200_OK)

class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        display_object = CustomerUserProfile.objects.get(user=user)
        context = {
            'id': display_object.id,
            'username': display_object.user.username,
            'email': display_object.user.email,
            'city': display_object.city
        }
        return Response(context, status=status.HTTP_200_OK)

class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return Response(context, status=status.HTTP_200_OK)

class BlogView(APIView):
    def post(self, request):
        
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Successfully Registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Categories(APIView):
    def get(self, request):
        serialiser = {}
        categories = Category.objects.all()
        if categories is None: 
            serializer.data = { 'empty': 'empty'}
        else: 
                    serializer = CategorySerializer(categories, many=True)  

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = CategorySerializer( data = request.data )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
                      
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
@ensure_csrf_cookie
def csrf_token_view(request):
    print(request.META.get('CSRF_COOKIE'))
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE')})