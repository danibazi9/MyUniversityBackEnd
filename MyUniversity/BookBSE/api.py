from rest_framework.views import APIView
from rest_framework.response import Response
from MyUniversity.models import Faculty, Field
from .serializers import FacultySerializer, FieldSerializer


class Faculties(APIView):
    def get(self, request):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)


class Fields(APIView):
    def get(self, request):
        fields = Field.objects.all()
        serializer = FieldSerializer(fields, many=True)
        print(serializer.data)
        # faculty = Faculty.objects.get(faculty_id=serializer.data[['faculty_']])
        # resp = serializer.data
        # resp['faculty'] = faculty
        print(serializer.data)
        return Response(serializer.data)