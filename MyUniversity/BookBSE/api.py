from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from MyUniversity.models import Faculty, Field, Book
from .serializers import FacultySerializer, FieldSerializer, BookSerializer


class Faculties(APIView):
    def get(self, request):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)


class Fields(APIView):
    def get(self, request, facultyID):
        if (facultyID != 0):
            fields = Field.objects.filter(faculty=facultyID)
        else:
            fields = Field.objects.all()

        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data)

class Books(APIView):
    def get(self, request):
        bookID = self.request.query_params.get('bookID', None)
        if (bookID != None):
            book = Book.objects.filter(book_id=bookID)
            serializer = BookSerializer(book, many=True)
            return Response(serializer.data)

        facultyID = self.request.query_params.get('facultyID', None)
        if (facultyID != None):
            book = Book.objects.filter(faculty=facultyID)
            serializer = BookSerializer(book, many=True)
            return Response(serializer.data)

        fieldID = self.request.query_params.get('fieldID', None)
        if (fieldID != None):
            book = Book.objects.filter(field=fieldID)
            serializer = BookSerializer(book, many=True)
            return Response(serializer.data)

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"INVALID REQUEST\n{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        bookID = self.request.query_params.get('bookID', None)
        if (bookID != None):
            book = Book.objects.get(book_id=bookID)
            if not book:
                return Response(f"NOT FOUND!\nINVALID ID={bookID}", status=status.HTTP_404_NOT_FOUND)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"INVALID REQUEST\n{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(f"INVALID ID: {bookID}", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        bookID = self.request.query_params.get('bookID', None)
        if (bookID != None):
            book = Book.objects.get(book_id=bookID)
            if not book:
                return Response(f"NOT FOUND!\nINVALID ID={bookID}", status=status.HTTP_404_NOT_FOUND)
            book.delete()
            return Response(f"DELETED SUCCESSFULLY\nID={bookID}", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("INVALID ID", status=status.HTTP_404_NOT_FOUND)