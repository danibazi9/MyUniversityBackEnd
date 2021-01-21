from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.serializers import *
from validate_email import validate_email
from account.models import Account
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import random


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        if validate_email(serializer.validated_data.get('email')):
            # if serializer.validated_data.get('email').endswith('.iust.ac.ir'):
                account = serializer.save()
                data['response'] = 'successful'
                token = Token.objects.get(user=account).key
                data['token'] = token
                data['user_id'] = account.user_id
                data['username'] = account.username
                data['first_name'] = account.first_name
                data['last_name'] = account.last_name
                data['email'] = account.email
                data['role'] = account.role
                return Response(data=data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response(f"The email '{serializer['email'].value}' isn't the academical university email",
            #                     status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(f"The email '{serializer['email'].value}' doesn't exist",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(('GET',))
def all_acounts_view(request):
    all_accounts = Account.objects.all()

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(all_accounts, many=True)
        return Response(serializer.data)


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {
            'token': token.key,
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }

        return Response(custom_response, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class logoutView(APIView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response("Successfully logged out!", status=status.HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Updating account has successfully done!'
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class SendEmail(APIView):
    def get(self, request):
        user_to_send_email = self.request.user

        random_code_generated = random.randrange(100000, 999999)

        template = render_to_string('account/email_template.html',
                                    {'name': user_to_send_email.first_name,
                                     'code': random_code_generated})

        email = EmailMessage(
            'Welcome to MyUniversity Platform!',
            template,
            'MyUniversity Organization',
            [user_to_send_email.email]
        )

        email.content_subtype = "html"
        email.fail_silently = False
        email.send()

        serializer = AccountPropertiesSerializer(user_to_send_email)
        json_response = {"email": serializer.data['email'], "vc_code": random_code_generated}
        return Response(json_response)
