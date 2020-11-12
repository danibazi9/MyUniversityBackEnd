from rest_framework import serializers
from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            # mobile_number=self['mobile_number'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']

        account.set_password(password)
        account.save()
        return account
