from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
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
        # print(f"Args: {arg}")
        # print("Query Params: ", self.request.query_params)

        facultyID = self.request.query_params.get('facultyID', None)
        # print(f"Faculty: {facultyID}")

        if facultyID != None:
            try:
                faculty = Faculty.objects.get(id=facultyID)
            except:
                faculty = None
            if faculty != None:
                # print("VERIFIED")
                fields = Field.objects.filter(faculty=facultyID)
                serializer = FieldSerializer(fields, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Faculty: {facultyID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Faculty: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)


class Books(APIView):
    def get(self, arg):
        bookID = self.request.query_params.get('bookID', None)
        if bookID != None:
            if bookID != '0':
                try:
                    book = Book.objects.get(id=bookID)
                except:
                    book = None
                # print("="*125, f"\nBook = {book}\n", "="*125)
                if book != None:
                    serializer = BookSerializer(book)
                    # print("=" * 125, f"\nBookSerializerData = {serializer.data}\n", "=" * 125)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(f"Book.BookID: {bookID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
                    # return Response(status=status.HTTP_200_OK)
            elif bookID == '0':
                books = Book.objects.all()
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.BookID: {bookID}, INVALID", status=status.HTTP_400_BAD_REQUEST)

        facultyID = self.request.query_params.get('facultyID', None)
        if facultyID != None:
            try:
                books = Book.objects.filter(faculty=Faculty.objects.get(id=facultyID).id)
            except:
                books = None
            if books != None:
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.FacultyID: {facultyID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

        fieldID = self.request.query_params.get('fieldID', None)
        if fieldID != None:
            try:
                books = Book.objects.filter(field=Field.objects.get(id=fieldID).id)
            except:
                books = None
            if books != None:
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.FieldID: {fieldID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)


        return Response("", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        serializer = BookSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        bookID = self.request.query_params.get('bookID', None)
        if (bookID != None):
            try:
                book = Book.objects.get(id=bookID)
            except:
                book = None
            if book == None:
                return Response(f"BookID={bookID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            serializer = BookSerializer(book, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("BookID: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        bookID = self.request.query_params.get('bookID', None)
        if (bookID != None):
            try:
                book = Book.objects.get(id=bookID)
            except:
                book = None
            if book == None:
                return Response(f"BookID={bookID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            book.delete()
            return Response(f"BookID: {bookID}, DELETED", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("BookID: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class Stocks(APIView):
    def get(self, arg):
        try:
            userID = self.request.user.user_id
        except:
            return Response(f"UserID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        state = self.request.query_params.get('state', None)
        if (state == 'sell'):
            stocks = Stock.objects.filter(seller=userID)
            serializer = StockSerializer(stocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif (state == 'buy'):
            stocks = Stock.objects.exclude(seller_id=userID)
            serializer = StockSerializer(stocks, many=True)
            return Response(serializer.data)
        elif (state == 'all'):
            stocks = Stock.objects.all()
            serializer = StockSerializer(stocks, many=True)
            return Response(serializer.data)
        else:
            stockID = self.request.query_params.get('stockID', None)
            if (stockID != None):
                stock = Stock.objects.get(id=stockID)
                serializer = StockSerializer(stock)
                return Response(serializer.data)
            else:
                return Response(f"SellerID: None OR BookID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    # def post(self, arg):
    #     user = self.request.user
    #     serializer = StockSerializer(data=self.request.data)
    #     if (serializer.is_valid()):
    #         print("="*50, f"\n{serializer}\n", "="*50)
    #         serializer.save()
    #         print("="*50, "\nDONE\n", "="*50)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(f"INVALID REQUEST\n{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
    #     # return Response(status=status.HTTP_200_OK)
