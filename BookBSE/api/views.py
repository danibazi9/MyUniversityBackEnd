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
                return Response(f"StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        user = self.request.user
        # print('='*25, f"\nUserHeader: {user}\n")
        serializer = StockSerializer(data=self.request.data)
        # print('='*25, f"\nSerializer: {serializer}\n")

        if (serializer.is_valid()):
            # print("="*50, f"\n{serializer}\n", "="*50)
            # print(f"SerializerValidatedData = {serializer.validated_data}")
            # print(f"SellerREQ: '{serializer.validated_data['seller']}'; UserREQ: '{user}'")
            if serializer.validated_data['seller'] == user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        stockID = self.request.query_params.get('stockID', None)
        if stockID != None:
            try:
                stock = Stock.objects.get(id=stockID)
            except:
                stock = None

            if stock != None:
                user = self.request.user
                print("="*50, f"\nUser: {user}; Stock.Seller: {stock.seller}")
                if stock.seller == user:
                    serializer = StockSerializer(stock, data=self.request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"StockID={stockID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        stockID = self.request.query_params.get('stockID', None)
        if stockID != None:
            try:
                stock = Stock.objects.get(id=stockID)
            except:
                stock = None

            if stock != None:
                user = self.request.user
                if stock.seller == user:
                    stock.delete()
                    return Response(f"StockID: {stockID}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"StockID={stockID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class Demands(APIView):
    def get(self, arg):
        state = self.request.query_params.get('state', None)
        if state != None:
            try:
                user = self.request.user
            except:
                return Response(f"UserID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            if state == 'client':
                sellers = Demand.objects.filter(client=user)
                serializer = DemandSerializer(sellers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif state == 'seller':
                applicants = Demand.objects.filter(seller=user)
                serializer = DemandSerializer(applicants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif state == 'all':
                demands = Demand.objects.all()
                serializer = DemandSerializer(demands, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"INVALID State: {state}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(f"State: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        user = self.request.user
        serializer = DemandSerializer(data=self.request.data)
        if serializer.is_valid():
            if serializer.validated_data['client'] == user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        demandID = self.request.query_params.get('demandID', None)
        user = self.request.user
        if demandID != None:
            try:
                demand = Demand.objects.get(id=demandID)
            except:
                demand = None
            if demand != None:
                if (demand.seller == user or
                    demand.client == user):
                    demand.delete()
                    return Response(f"DemandID: {demandID}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"DemandID={demandID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

        bookID = self.request.query_params.get('bookID', None)
        state = self.request.query_params.get('state', None)
        if (bookID != None and state != None):
            try:
                book = Book.objects.get(id=bookID)
            except:
                book = None
            if book != None:
                if state == 'seller':
                    try:
                        demands = Demand.objects.filter(seller=user, book=bookID)
                    except:
                        demands = None
                    if demands != None:
                        demands.delete()
                        return Response(f"Demands, Seller: {user} AND Book: {bookID}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {bookID}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                elif state == 'client':
                    try:
                        demands = Demand.objects.filter(client=user, book=bookID)
                    except:
                        demands = None
                    if demands != None:
                        demands.delete()
                        return Response(f"Demands, Client: {user} AND Book: {bookID}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {bookID}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                elif state == 'all':
                    try:
                        demands = Demand.objects.filter(Q(client=user) | Q(seller=user), book=bookID)
                    except:
                        demands = None
                    if demands != None:
                        demands.delete()
                        return Response(f"Demands, Seller/Client: {user}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {bookID}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(f"INVALID State: {state}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            elif (bookID == None and state == 'all'):
                demands = Demand.objects.filter(Q(client=user) | Q(seller=user))
                demands.delete()
                return Response(f"Demands, Seller/Client: {user}, DELETED",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(f"BookID={bookID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("(DemandID: None) OR (BookID: None OR State: None), BAD REQUEST",
                            status=status.HTTP_400_BAD_REQUEST)