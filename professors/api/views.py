import base64
import json

from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from BookBSE.api.serializer import FacultySerializer
from .serializer import *

from ..models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_professors(request):
    faculty_id = request.query_params.get('faculty_id', None)
    search = request.query_params.get('search', None)

    if faculty_id is not None:
        try:
            Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response(f"Faculty with faculty_id {faculty_id} NOT FOUND!")

    if faculty_id is not None:
        if search is None:
            professors_to_show = Professor.objects.filter(faculty__id=faculty_id)
        else:
            professors_to_show = Professor.objects.filter(Q(faculty__id=faculty_id),
                                                          Q(first_name__icontains=search) |
                                                          Q(last_name__icontains=search) |
                                                          Q(academic_rank__icontains=search) |
                                                          Q(research_axes__subject__icontains=search)
                                                          )
        serializer = ProfessorSerializer(professors_to_show, many=True)

        data = json.loads(json.dumps(serializer.data))
        return Response(data, status=status.HTTP_200_OK)
    else:
        if search is None:
            professors_to_show = Professor.objects.all()
        else:
            professors_to_show = Professor.objects.filter(Q(first_name__icontains=search) |
                                                          Q(last_name__icontains=search) |
                                                          Q(faculty__name__icontains=search) |
                                                          Q(academic_rank__icontains=search) |
                                                          Q(research_axes__subject__icontains=search)
                                                          )
        serializer = ProfessorSerializer(professors_to_show, many=True)

        data = json.loads(json.dumps(serializer.data))
        return Response(data, status=status.HTTP_200_OK)

