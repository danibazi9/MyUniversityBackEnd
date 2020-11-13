from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
from BookBSE.models import *
from BookBSE.api.serializer import *
from django.db.models import Q


class Faculties(APIView):
    def get(self, arg):
        print(f"Args: {arg}")
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

class Fields(APIView):
    def get(self, arg):
        print(f"Args: {arg}")
        print("Query Params: ", self.request.query_params)

        facultyID = self.request.query_params.get('facultyID', None)
        print(f"Faculty: {facultyID}")

        if facultyID != None:
            if Faculty.objects.get(id=facultyID) != None:
                print("VERIFIED")
                fields = Field.objects.filter(faculty=facultyID)
                serializer = FieldSerializer(fields, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Faculty: {facultyID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Faculty: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)