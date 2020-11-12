from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.serializers import RegistrationSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token
from validate_email import validate_email
from account.models import Account


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
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
        return Response(f"The email '{serializer['email'].value}' doesn't exist",
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
            data['response'] = 'Account update success'
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
