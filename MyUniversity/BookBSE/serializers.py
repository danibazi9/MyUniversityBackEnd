from rest_framework import serializers
from MyUniversity.models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"