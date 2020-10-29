import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . serializers import *

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from validate_email import validate_email


def get_user(stuID):
    try:
        user_to_find = User.objects.get(student_id=stuID)
        return user_to_find
    except User.DoesNotExist:
        return None

