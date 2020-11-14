from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.serializers import RegistrationSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token
from validate_email import validate_email
from account.models import Account
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import random


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    print(serializer)
    if serializer.is_valid():
        email = request.data['email']
        if validate_email(serializer.validated_data.get('email')):
            account = serializer.save()
            data['response'] = 'successful'
            token = Token.objects.get(user=account).key
            data['token'] = token
            return Response(data=data, status=status.HTTP_201_CREATED)
            # if serializer.validated_data.get('email').endswith('.iust.ac.ir'):
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response(f"The email '{serializer['email'].value}' isn't the academical university email",
            #                     status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(f"The email '{serializer['email'].value}' doesn't exist",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(f"Not acceptable",
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', ])
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(['GET', ])
def all_accounts(request):
    users = Account.objects.all()
    serializer = AccountPropertiesSerializer(users, many=True)
    print(users)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
        print(account.email)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Account update success'
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = Account.objects.get(email=request.user.email)
        return user


class SendEmail(APIView):
    def get(self, request):
        user_to_send_email = get_user(request)
        if not user_to_send_email:
            return Response(f"User was Not Found!", status=status.HTTP_404_NOT_FOUND)

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
        json_responsed = {"email": serializer.data['email'], "vc_code": random_code_generated}
        return Response(json_responsed)