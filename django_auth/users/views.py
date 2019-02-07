import jwt
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
# from usersexample.models import Profile
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, LoginSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.models import User
# from rest_framework.request import Request
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView  # Used for a create-only endpoints, provides a post method handler
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView  # Taking the views of REST framework Request & Response

# import django_auth.users.serializers
from .tokens import account_activation_token

# from django_auth.users.tokens import account_activation_token
# from django_auth.users.tokens import account_activation_token
from .forms import SignupForm

from .models import User
# from .serializers import UserSerializer, LoginSerializer


def home(request):
    return render(request, "home.html", {})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.object.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return render(request, 'login.html')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request, 'login.html', {'form': form})
    else:
        return HttpResponse('Activation link is invalid!')


def get_jwt_token(user):
    jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler=api_settings.JWT_ENCODE_HANDLER
    payload=jwt_payload_handler(user)
    print(payload)
    print(jwt_payload_handler(payload))
    return jwt_encode_handler(payload)

# def user_login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user():
#             login(request,user)
#             jwt_token=get_jwt_token(user)
#             url='/home/'
#             response=redirect(url)
#             response['Token']=jwt_token
#             return response
#         else:
#             return HttpResponse(messages.sucecess(request,"Your account was inactive"))
#     else:
#         messages.sucecess(request,"Invalid")
#         return redirect("login")
#




# def login(self, request):
        # try:
        #     first_name = request.POST.get('first_name')
        #     password = request.POST.get('password')
        #     # user = authenticate(email=email, password=password)
        #     user = User.object.get(first_name=first_name, password=password)
        #     if user:
        #         try:
        #             payload = {
        #                 'email': first_name,
        #                 'password': password,
        #             }
        #             # token = {'token': jwt.encode(payload,'SECRET')}
        #             token = jwt.encode(payload, 'SECRET')
        #             return HttpResponse(token, {})
        #         except Exception as e:
        #             raise e
        # except Exception as e:
        #     res = {'error': 'please provide an valid email and a password'}
        #     return HttpResponse(res)
        # return render(request, 'user_token.html')

def login(self, request):
    return render(request, 'user_token.html')
#

# class ProfileList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'register.html'
#
#     def post(self, request):
#         queryset = User.object.all()
#         return Response({'users': queryset})
#
#
# class ProfileDetail(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'profile_detail.html'
#
#     def get(self, request):
#         profile = get_object_or_404(User)
#         serializer = UserSerializer(profile)
#         queryset = User.object.all()
#         return Response({'serializer': serializer, 'profile': profile})
#         # return Response({'users': queryset})
#
#     def post(self, request, pk):
#         profile = get_object_or_404(User)
#         serializer = UserSerializer(profile, data=request.data)
#         if not serializer.is_valid():
#             return Response({'serializer': serializer, 'profile': profile})
#         serializer.save()
#         return redirect('profile-list')


# def register(request):
#     serializer_class = UserSerializer
#     queryset = User.object.all()
#     return render(request, "register.html", {})


#   return HttpResponse('home.html',{})

class CreateUserAPIView(CreateAPIView):  # Created the view class for a registeration
    serializer_class = UserSerializer  # The serializer class that should be used for validating and
    # deseria lizing input, and for serializing output
    # email = serializers.EmailField(validators=[UniqueValidator()])
    queryset = User.object.all()  # The queryset that should be used for returning objects from this view.


import json
class LoginView(APIView):
    serializer_class = LoginSerializer
    queryset = User.object.all()
    print(queryset)
    http_method_names = ['post', 'get']

    def post(self, request):
        try:
            if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                # print(first_name)
                print(password)
                user = authenticate(username=username, password=password)
                #user = User.object.get(first_name=first_name, password=password)
                print(user, "fdsfsd")
                if user():
                    if user.is_active():
                        try:
                            payload = {
                                'username': username,
                                'password': password,
                            }
                            # token = {'token': jwt.encode(payload,'SECRET')}
                            token = jwt.encode(payload, 'SECRET')
                            # return Response(token, {})
                            print(token)
                            return HttpResponse(token,{})
                            # return HttpResponse("<h1>login success</>",{})

                        except Exception as e:
                            raise e
            else:
                # res = {'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response("User Not Found", status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            res = {'error': 'please provide an valid email and a password'}
            return Response(res)
