import json

from rest_framework import status
from rest_framework.parsers import FileUploadParser
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

        if facultyID is not None:
            try:
                faculty = Faculty.objects.get(id=facultyID)
            except:
                faculty = None
            if faculty is not None:
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
        if bookID is not None:
            if bookID != '0':
                try:
                    book = Book.objects.get(id=bookID)
                except:
                    book = None
                # print("="*125, f"\nBook = {book}\n", "="*125)
                if book is not None:
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
        if facultyID is not None:
            try:
                books = Book.objects.filter(faculty=Faculty.objects.get(id=facultyID).id)
            except:
                books = None
            if books is not None:
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.FacultyID: {facultyID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

        fieldID = self.request.query_params.get('fieldID', None)
        if fieldID is not None:
            try:
                books = Book.objects.filter(field=Field.objects.get(id=fieldID).id)
            except:
                books = None
            if books is not None:
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
        if bookID is not None:
            try:
                book = Book.objects.get(id=bookID)
            except:
                book = None
            if book is None:
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
        if bookID is not None:
            try:
                book = Book.objects.get(id=bookID)
            except:
                book = None
            if book is None:
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
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        state = self.request.query_params.get('state', None)
        if state == 'sell':
            stocks = Stock.objects.filter(seller=userID)
            serializer = AllStockSerializer(stocks, many=True)
            data = json.loads(json.dumps(serializer.data))
            for x in data:
                for key in x['book'].keys():
                    x[key] = x['book'][key]
                del x['book']
            return Response(data, status=status.HTTP_200_OK)
        elif state == 'buy':
            stocks = Stock.objects.exclude(seller=userID)
            serializer = AllStockSerializer(stocks, many=True)
            data = json.loads(json.dumps(serializer.data))
            for x in data:
                for key in x['book'].keys():
                    x[key] = x['book'][key]
                del x['book']
            return Response(data)
        elif state == 'all':
            stocks = Stock.objects.all()  # .prefetch_related('book')
            serializer = AllStockSerializer(stocks, many=True)
            data = json.loads(json.dumps(serializer.data))
            for x in data:
                for key in x['book'].keys():
                    x[key] = x['book'][key]
                del x['book']
            return Response(data)
        else:
            stockID = self.request.query_params.get('stockID', None)
            if stockID is not None:
                stock = Stock.objects.get(id=stockID)
                serializer = StockSerializerStockID(stock)
                data = json.loads(json.dumps(serializer.data))
                for key in data['book'].keys():
                    data[key] = data['book'][key]
                del data['book']
                return Response(data)
            else:
                return Response(f"StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        user = self.request.user
        serializer = StockSerializer(data=self.request.data)

        if serializer.is_valid():
            if serializer.validated_data['seller'] == user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("ACCESS DENIED!", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        stockID = self.request.query_params.get('stockID', None)
        if stockID is not None:
            try:
                stock = Stock.objects.get(id=stockID)
            except:
                stock = None

            if stock is not None:
                user = self.request.user
                print("=" * 50, f"\nUser: {user}; Stock.Seller: {stock.seller}")
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
        if stockID is not None:
            try:
                stock = Stock.objects.get(id=stockID)
            except:
                stock = None

            if stock is not None:
                user = self.request.user
                if stock.seller == user:
                    stock.delete()
                    return Response(f"StockID: {stockID}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response("ACCESS DENIED!", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"StockID={stockID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class Demands(APIView):
    def get(self, arg):
        state = self.request.query_params.get('state', None)
        if state is not None:
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
        if demandID is not None:
            try:
                demand = Demand.objects.get(id=demandID)
            except:
                demand = None
            if demand is not None:
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
        if bookID is not None and state is not None:
            try:
                book = Book.objects.get(id=bookID)
            except:
                book = None
            if book is not None:
                if state == 'seller':
                    try:
                        demands = Demand.objects.filter(seller=user, book=bookID)
                    except:
                        demands = None
                    if demands is not None:
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
                    if demands is not None:
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
                    if demands is not None:
                        demands.delete()
                        return Response(f"Demands, Seller/Client: {user}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {bookID}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(f"INVALID State: {state}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            elif bookID is None and state == 'all':
                demands = Demand.objects.filter(Q(client=user) | Q(seller=user))
                demands.delete()
                return Response(f"Demands, Seller/Client: {user}, DELETED",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(f"BookID={bookID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("(DemandID: None) OR (BookID: None OR State: None), BAD REQUEST",
                            status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class Trades(APIView):
    def get(self, arg):
        user = self.request.user
        tradeID = self.request.query_params.get('tradeID', None)
        if tradeID is not None:
            try:
                trade = Trade.objects.get(id=tradeID)
            except:
                trade = None
            if trade is not None:
                if trade.seller == user or trade.buyer == user:
                    serializer = TradeSerializer(trade)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"TradeID: {tradeID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            state = self.request.query_params.get('state', None)
            if state is not None:
                if state == 'seller':
                    sells = Trade.objects.filter(seller=user)
                    serializer = TradeSerializer(sells, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    for x in data:
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    return Response(data, status=status.HTTP_200_OK)
                elif state == 'buyer':
                    buies = Trade.objects.filter(buyer=user)
                    serializer = TradeSerializer(buies, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    for x in data:
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    return Response(data, status=status.HTTP_200_OK)
                elif state == 'all':
                    trades = Trade.objects.filter(Q(seller=user) | Q(buyer=user))
                    serializer = TradeSerializer(trades, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    for x in data:
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(f"INVALID State: {state}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("State: None OR TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        serializer = TradeSerializer(data=self.request.data)
        user = self.request.user
        if serializer.is_valid():
            sellerID = serializer.validated_data['seller']
            bookID = serializer.validated_data['book']

            if sellerID == user:
                try:
                    clients = Demand.objects.filter(seller=sellerID, book=bookID)
                    clients.delete()
                except:
                    print(f"Clients, Seller: {sellerID}, Book: {bookID}, NOT FOUND")
                try:
                    stock = Stock.objects.get(seller=sellerID, book=bookID)
                    stock.delete()
                except:
                    print(f"Clients, Seller: {sellerID}, Book: {bookID}, NOT FOUND")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        tradeID = self.request.query_params.get('tradeID', None)
        if tradeID is not None:
            try:
                trade = Trade.objects.get(id=tradeID)
            except:
                trade = None
            if trade is not None:
                serializer = TradeSerializer(trade, data=self.request.data)
                user = self.request.user
                if serializer.is_valid():
                    if serializer.validated_data['seller'] == user:
                        if trade.state == False:
                            if serializer.validated_data['state'] == True and \
                                    serializer.validated_data['trade'] is not None:
                                trade.state = serializer.validated_data['state']
                                trade.trade = serializer.validated_data['trade']
                                trade.description = serializer.validated_data['description']
                                trade.save()
                                return Response(serializer.data, status=status.HTTP_200_OK)
                            else:
                                return Response(f"NO CHANGES APPLIED", status=status.HTTP_200_OK)
                        else:
                            return Response("ACCESS DENIED, TRADE DONE", status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f"TradeID={tradeID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        tradeID = self.request.query_params.get('tradeID', None)
        if tradeID is not None:
            try:
                trade = Trade.objects.get(id=tradeID)
            except:
                trade = None
            if trade is not None:
                user = self.request.user
                if trade.seller == user:
                    if not trade.state:
                        trade.delete()
                        return Response(f"Trade: {tradeID}, DELETED", status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response("ACCESS DENIED, TRADE DONE", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"TradeID={tradeID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class StocksHistory(APIView):
    def get(self, arg):
        try:
            user = self.request.user
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        try:
            stocks = Stock.objects.filter(seller=user)
        except:
            stocks = None
        if stocks is not None:
            serializer = StocksHistorySerializer(stocks, many=True)
            data = json.loads(json.dumps(serializer.data))
            for x in data:
                for key in x['book'].keys():
                    x[key] = x['book'][key]
                del x['book']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(f"Stocks: seller {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)


@permission_classes((IsAuthenticated,))
class TradesHistory(APIView):
    def get(self, arg):
        try:
            user = self.request.user
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        state = self.request.query_params.get('state', None)
        if state is not None:
            if state == 'all':
                try:
                    trades = Trade.objects.filter(Q(seller=user) | Q(buyer=user), state=True)
                except:
                    trades = None
                if trades is not None:
                    serializer = TradesHistorySerializer(trades, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    for x in data:
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(f"Trades, Seller/Buyer: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            elif state == 'seller':
                try:
                    trades = Trade.objects.filter(seller=user, state=True)
                except:
                    trades = None
                if trades is not None:
                    serializer = TradesHistorySerializer(trades, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    for x in data:
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(f"Trades, Seller/Buyer: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            elif state == 'buyer':
                try:
                    trades = Trade.objects.filter(buyer=user, state=True)
                except:
                    trades = None
                if trades is not None:
                    serializer = TradesHistorySerializer(trades, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    for x in data:
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(f"Trades, Seller/Buyer: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("State: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class ReportProblems(APIView):
    def get(self, arg):
        user = self.request.user
        reportID = self.request.query_params.get('reportID', None)
        if reportID is not None:
            try:
                report = ReportProblem.objects.get(id=reportID)
                if report.accuser == user or report.accused:
                    serializer = ReportProblemSerializer(report)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            except:
                return Response(f"ReportProblem: {reportID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            state = self.request.query_params.get('state', None)
            if state is not None:
                if state == 'all':
                    try:
                        reports = ReportProblem.objects.filter(Q(accuser=user) | Q(accused=user))
                    except:
                        reports = None
                    if reports is not None:
                        serializer = ReportProblemSerializer(reports, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(f"Reports, Accuser/Accused: {user}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                elif state == 'accuser':
                    try:
                        reports = ReportProblem.objects.filter(accuser=user)
                    except:
                        reports = None
                    if reports is not None:
                        serializer = ReportProblemSerializer(reports, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(f"Reports, Accuser: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
                elif state == 'accused':
                    try:
                        reports = ReportProblem.objects.filter(accused=user)
                    except:
                        reports = None
                    if reports is not None:
                        serializer = ReportProblemSerializer(reports, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(f"Reports, Accused: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("State: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        tradeID = self.request.query_params.get('tradeID', None)
        user = self.request.user

        if tradeID is not None:
            try:
                trade = Trade.objects.get(id=tradeID)
                # print("="*50 ,f"Trade: {Trade.objects.get(id=tradeID)}")
                if trade.state:
                    if trade.seller == user or trade.buyer == user:
                        serializer = ReportProblemSerializer(data=self.request.data)
                        # print("=" * 50, f"ENTER")
                        if serializer.is_valid():
                            if serializer.validated_data['accuser'] == user:
                                serializer.save()
                                return Response(serializer.data, status=status.HTTP_200_OK)
                            else:
                                return Response(f"Accuser != Req.User, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(f"ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response(f"ACCESS DENIED, TRADE DONE", status=status.HTTP_403_FORBIDDEN)
            except:
                return Response(f"Trade: {tradeID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        reportID = self.request.query_params.get('reportID', None)
        user = self.request.user

        if reportID is not None:
            try:
                report = ReportProblem.objects.get(id=reportID)
                if report.accuser == user:
                    serializer = ReportProblemSerializer(report, data=self.request.data)
                    if serializer.is_valid():
                        if serializer.validated_data['accuser'] == user:
                            report.text = serializer.validated_data['text']
                            report.save()
                            # print("="*50)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response(f"Accuser != Req.User, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(f"ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            except:
                return Response(f"Report: {reportID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("ReportID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        reportID = self.request.query_params.get('reportID', None)
        user = self.request.user

        if reportID is not None:
            try:
                report = ReportProblem.objects.get(id=reportID)
                if report.accuser == user:
                    report.delete()
                    return Response(f"Report: {reportID}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(f"ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            except:
                return Response(f"Report: {reportID}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("ReportID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


# =========================================================
@permission_classes((IsAuthenticated,))
class StocksSO(APIView):
    def get(self, arg):
        search = self.request.query_params.get('search', None)
        orderby = self.request.query_params.get('orderby', 'asc')

        if search is not None:
            if orderby == 'asc':
                try:
                    stocks = Stock.objects.filter(book__name__icontains=search).order_by('upload')
                    serializer = StockSerializer(stocks, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif orderby == 'dec':
                try:
                    stocks = Stock.objects.filter(book__name__icontains=search).order_by('-upload')
                    serializer = StockSerializer(stocks, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("Search: None, BADREQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class TradesSO(APIView):
    def get(self, arg):
        search = self.request.query_params.get('search', None)
        orderby = self.request.query_params.get('orderby', 'asc')

        if search is not None:
            if orderby == 'asc':
                try:
                    trades = Trade.objects.filter(book__name__icontains=search).order_by('upload')
                    serializer = StockSerializer(trades, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            elif orderby == 'dec':
                try:
                    trades = Trade.objects.filter(book__name__icontains=search).order_by('-upload')
                    serializer = StockSerializer(trades, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("Search: None, BADREQUEST", status=status.HTTP_400_BAD_REQUEST)
