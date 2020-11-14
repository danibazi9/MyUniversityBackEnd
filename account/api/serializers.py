from rest_framework import serializers
from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'student_id', 'mobile_number', 'password']

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            student_id=self.validated_data['student_id'],
            mobile_number=self.validated_data['mobile_number'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']

        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'email', 'username', 'student_id', 'first_name', 'last_name', 'mobile_number']
