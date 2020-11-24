import json

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from BookBSE.models import *
from BookBSE.api.serializer import *
from django.db.models import Q


class Faculties(APIView):
    def get(self, arg):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)


class Fields(APIView):
    def get(self, arg):
        # print(f"Args: {arg}")
        # print("Query Params: ", self.request.query_params)

        faculty_id = self.request.query_params.get('facultyID', None)
        # print(f"Faculty: {facultyID}")

        if faculty_id is not None:
            try:
                faculty = Faculty.objects.get(id=faculty_id)
            except Faculty.DoesNotExist:
                faculty = None
            if faculty is not None:
                # print("VERIFIED")
                fields = Field.objects.filter(faculty=faculty_id)
                serializer = FieldSerializer(fields, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Faculty: {faculty_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Faculty: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)


class Books(APIView):
    def get(self, arg):
        book_id = self.request.query_params.get('bookID', None)
        if book_id is not None:
            if book_id != '0':
                try:
                    book = Book.objects.get(id=book_id)
                except Book.DoesNotExist:
                    book = None
                # print("="*125, f"\nBook = {book}\n", "="*125)
                if book is not None:
                    serializer = BookSerializer(book)
                    # print("=" * 125, f"\nBookSerializerData = {serializer.data}\n", "=" * 125)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(f"Book.BookID: {book_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
                    # return Response(status=status.HTTP_200_OK)
            elif book_id == '0':
                books = Book.objects.all()
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.BookID: {book_id}, INVALID", status=status.HTTP_400_BAD_REQUEST)

        faculty_id = self.request.query_params.get('facultyID', None)
        if faculty_id is not None:
            try:
                books = Book.objects.filter(faculty=Faculty.objects.get(id=faculty_id).id)
            except Book.DoesNotExist:
                books = None
            if books is not None:
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.FacultyID: {faculty_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

        field_id = self.request.query_params.get('fieldID', None)
        if field_id is not None:
            try:
                books = Book.objects.filter(field=Field.objects.get(id=field_id).id)
            except Book.DoesNotExist:
                books = None
            if books is not None:
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(f"Book.FieldID: {field_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        return Response("", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        serializer = BookSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        book_id = self.request.query_params.get('bookID', None)
        if book_id is not None:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                book = None
            if book is None:
                return Response(f"BookID={book_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            serializer = BookSerializer(book, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("BookID: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        book_id = self.request.query_params.get('bookID', None)
        if book_id is not None:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                book = None
            if book is None:
                return Response(f"BookID={book_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            book.delete()
            return Response(f"BookID: {book_id}, DELETED", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("BookID: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class Stocks(APIView):
    def get(self, arg):
        # getting params from url link
        stock_id = self.request.query_params.get('stockID', None)
        if stock_id is not None:
            stock = Stock.objects.get(id=stock_id)
            serializer = StockSerializerStockID(stock)
            data = json.loads(json.dumps(serializer.data))
            for key in data['book'].keys():
                data[key] = data['book'][key]
            del data['book']
            return Response(data)
        else:
            search = self.request.query_params.get('search', None)
            min = self.request.query_params.get('min', None)
            max = self.request.query_params.get('max', None)
            faculty = self.request.query_params.get('faculty', None)
            print('search: ', search)
            print('min: ', min)
            print('max: ', max)
            print('faculty: ', faculty)
            # checking for a token from user
            try:
                user_id = self.request.user.user_id
            except:
                return Response(f"UserID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            print(self.request.query_params)
            if search is None and min is None and faculty is None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id))
            elif search is None and min is None and faculty is not None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), book__faculty__name=faculty )
            elif search is None and min is not None and faculty is None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), price__gte=min, price__lte=max)
            elif search is not None and min is None and faculty is None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), book__name__icontains=search)
            elif search is None and min is not None and faculty is not None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), price__gte=min, price__lte=max, book__faculty__name=faculty)
            elif search is not None and min is None and faculty is not None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), book__name__icontains=search, book__faculty__name=faculty)
            elif search is not None and min is not None and faculty is None:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), price__gte=min, price__lte=max, book__name__icontains=search)
            else:
                stocks = Stock.objects.filter(~Q(seller_id=user_id), price__gte=min, price__lte=max,
                                              book__name__icontains=search, book__faculty__name=faculty)
            serializer = AllStockSerializer(stocks, many=True)
            data = json.loads(json.dumps(serializer.data))
            print(data)
            for x in data:
                for key in x['book'].keys():
                    x[key] = x['book'][key]
                    x['seller_username'] = Account.objects.get(user_id=x['seller']).username
                del x['book']
            return Response(data)

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
        stock_id = self.request.query_params.get('stockID', None)
        if stock_id is not None:
            try:
                stock = Stock.objects.get(id=stock_id)
            except Stock.DoesNotExist:
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
                return Response(f"StockID={stock_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        stock_id = self.request.query_params.get('stockID', None)
        if stock_id is not None:
            try:
                stock = Stock.objects.get(id=stock_id)
            except Stock.DoesNotExist:
                stock = None

            if stock is not None:
                user = self.request.user
                if stock.seller == user:
                    stock.delete()
                    return Response(f"StockID: {stock_id}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response("ACCESS DENIED!", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"StockID={stock_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("StockID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


class DemandAcceptor(APIView):
    def post(self, arg):
        map = self.request.data
        stock_id = map['stock_id']
        print(map)
        demands = Demand.objects.filter(stock_id=stock_id)
        demands.delete()
        # print(demands['seller'])
        trade = Trade()
        trade.book = Book.objects.get(id=map['book'])
        trade.seller = Account.objects.get(user_id=map['seller'])
        trade.buyer = Account.objects.get(user_id=map['client'])
        trade.image = map['image']
        trade.state = map['state']
        trade.description = map['description']
        trade.price = map['price']
        trade.save()
        stock = Stock.objects.get(id=stock_id)
        stock.delete()
        # print('trade is: ', trade)
        # demands = Demand.objects.filter(seller_id=map['seller'])
        # demands.delete()
        return Response('deleted', status=status.HTTP_200_OK)


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
                demands = Demand.objects.filter(client=user)
            elif state == 'seller':
                demands = Demand.objects.filter(seller=user)
            elif state == 'all':
                demands = Demand.objects.filter(Q(client=user) | Q(seller=user))
            else:
                return Response(f"State: Invalid state, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
            serializer = DemandSerializer(demands, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            data = json.loads(json.dumps(serializer.data))
            for x in data:
                x['seller_username'] = Account.objects.get(user_id=x['seller']).username
                x['client_username'] = Account.objects.get(user_id=x['client']).username
                for key in x['book'].keys():
                    x[key] = x['book'][key]
                del x['book']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(f"State: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        user = self.request.user
        serializer = DemandPostSerializer(data=self.request.data)
        if serializer.is_valid():
            if serializer.validated_data['client'] == user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        demand_id = self.request.query_params.get('demandID', None)
        user = self.request.user
        if demand_id is not None:
            try:
                demand = Demand.objects.get(id=demand_id)
            except Demand.DoesNotExist:
                demand = None
            if demand is not None:
                if (demand.seller == user or
                        demand.client == user):
                    demand.delete()
                    return Response(f"DemandID: {demand_id}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"DemandID={demand_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

        book_id = self.request.query_params.get('bookID', None)
        state = self.request.query_params.get('state', None)
        if book_id is not None and state is not None:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                book = None
            if book is not None:
                if state == 'seller':
                    try:
                        demands = Demand.objects.filter(seller=user, book=book_id)
                    except Demand.DoesNotExist:
                        demands = None
                    if demands is not None:
                        demands.delete()
                        return Response(f"Demands, Seller: {user} AND Book: {book_id}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {book_id}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                elif state == 'client':
                    try:
                        demands = Demand.objects.filter(client=user, book=book_id)
                    except Demand.DoesNotExist:
                        demands = None
                    if demands is not None:
                        demands.delete()
                        return Response(f"Demands, Client: {user} AND Book: {book_id}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {book_id}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                elif state == 'all':
                    try:
                        demands = Demand.objects.filter(Q(client=user) | Q(seller=user), book=book_id)
                    except Demand.DoesNotExist:
                        demands = None
                    if demands is not None:
                        demands.delete()
                        return Response(f"Demands, Seller/Client: {user}, DELETED",
                                        status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response(f"Demands, Seller: {user} AND Book: {book_id}, NOT FOUND",
                                        status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(f"INVALID State: {state}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            elif book_id is None and state == 'all':
                demands = Demand.objects.filter(Q(client=user) | Q(seller=user))
                demands.delete()
                return Response(f"Demands, Seller/Client: {user}, DELETED",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(f"BookID={book_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("(DemandID: None) OR (BookID: None OR State: None), BAD REQUEST",
                            status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class Trades(APIView):
    # def delete_demands(self, seller_id, client_id, book_id):

    def get(self, arg):
        user = self.request.user
        trade_id = self.request.query_params.get('tradeID', None)
        if trade_id is not None:
            try:
                trade = Trade.objects.get(id=trade_id)
            except Trade.DoesNotExist:
                trade = None
            if trade is not None:
                if trade.seller == user or trade.buyer == user:
                    serializer = TradeSerializer(trade)
                    data = json.loads(json.dumps(serializer.data))
                    map = data['book']
                    keys = list(map.keys())
                    values = list(map.values())
                    data['seller_username'] = Account.objects.get(user_id=data['seller']).username
                    data['client_username'] = Account.objects.get(user_id=data['buyer']).username
                    for x in range(0, len(keys)):
                        data[keys[x]] = values[x]
                    del data['book']
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"TradeID: {trade_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
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
                    # trades = Trade.objects.filter(Q(seller=user) | Q(buyer=user))
                    trades = Trade.objects.filter(Q(seller=user) | Q(buyer=user))
                    serializer = TradeSerializer(trades, many=True)
                    data = json.loads(json.dumps(serializer.data))
                    # for x in data:
                    #     for key in x['book'].keys():
                    #         x[key] = x['book'][key]
                    #     del x['book']
                    for x in data:
                        x['seller_username'] = Account.objects.get(user_id=x['seller']).username
                        x['client_username'] = Account.objects.get(user_id=x['buyer']).username
                        for key in x['book'].keys():
                            x[key] = x['book'][key]
                        del x['book']
                    # return Response(data, status=status.HTTP_200_OK)
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(f"INVALID State: {state}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("State: None OR TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        serializer = TradeSerializer(data=self.request.data)
        user = self.request.user
        if serializer.is_valid():
            seller_id = serializer.validated_data['seller']
            book_id = serializer.validated_data['book']

            if seller_id == user:
                try:
                    clients = Demand.objects.filter(seller=seller_id, book=book_id)
                    clients.delete()
                except Demand.DoesNotExist:
                    print(f"Clients, Seller: {seller_id}, Book: {book_id}, NOT FOUND")
                try:
                    stock = Stock.objects.get(seller=seller_id, book=book_id)
                    stock.delete()
                except Stock.DoesNotExist:
                    print(f"Clients, Seller: {seller_id}, Book: {book_id}, NOT FOUND")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        trade_id = self.request.query_params.get('tradeID', None)
        map = self.request.data
        state = map['state']
        print(state)
        if trade_id is not None:
            try:
                trade = Trade.objects.get(id=trade_id)
                print(trade)
            except Trade.DoesNotExist:
                trade = None
            if trade is not None:
                serializer = TradeSerializer(trade, data=self.request.data)
                user = self.request.user
                if serializer.is_valid():
                    if serializer.validated_data['seller'] == user:
                        if not trade.state:
                            trade.state = state
                            trade.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response("ACCESS DENIED, TRADE DONE", status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f"TradeID={trade_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        trade_id = self.request.query_params.get('tradeID', None)
        if trade_id is not None:
            try:
                trade = Trade.objects.get(id=trade_id)
            except Trade.DoesNotExist:
                trade = None
            if trade is not None:
                user = self.request.user
                if trade.seller == user:
                    if not trade.state:
                        trade.delete()
                        return Response(f"Trade: {trade_id}, DELETED", status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response("ACCESS DENIED, TRADE DONE", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(f"TradeID={trade_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
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
        except Stock.DoesNotExist:
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
                except Trade.DoesNotExist:
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
                except Trade.DoesNotExist:
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
                except Trade.DoesNotExist:
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
        report_id = self.request.query_params.get('reportID', None)
        if report_id is not None:
            try:
                report = ReportProblem.objects.get(id=report_id)
                if report.accuser == user or report.accused:
                    serializer = ReportProblemSerializer(report)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            except ReportProblem.DoesNotExist:
                return Response(f"ReportProblem: {report_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            state = self.request.query_params.get('state', None)
            if state is not None:
                if state == 'all':
                    try:
                        reports = ReportProblem.objects.filter(Q(accuser=user) | Q(accused=user))
                    except ReportProblem.DoesNotExist:
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
                    except ReportProblem.DoesNotExist:
                        reports = None
                    if reports is not None:
                        serializer = ReportProblemSerializer(reports, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(f"Reports, Accuser: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
                elif state == 'accused':
                    try:
                        reports = ReportProblem.objects.filter(accused=user)
                    except ReportProblem.DoesNotExist:
                        reports = None
                    if reports is not None:
                        serializer = ReportProblemSerializer(reports, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(f"Reports, Accused: {user}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("State: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, arg):
        trade_id = self.request.query_params.get('tradeID', None)
        user = self.request.user

        if trade_id is not None:
            try:
                trade = Trade.objects.get(id=trade_id)
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
            except Trade.DoesNotExist:
                return Response(f"Trade: {trade_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("TradeID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        report_id = self.request.query_params.get('reportID', None)
        user = self.request.user

        if report_id is not None:
            try:
                report = ReportProblem.objects.get(id=report_id)
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
            except ReportProblem.DoesNotExist:
                return Response(f"Report: {report_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("ReportID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        report_id = self.request.query_params.get('reportID', None)
        user = self.request.user

        if report_id is not None:
            try:
                report = ReportProblem.objects.get(id=report_id)
                if report.accuser == user:
                    report.delete()
                    return Response(f"Report: {report_id}, DELETED", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(f"ACCESS DENIED", status=status.HTTP_403_FORBIDDEN)
            except ReportProblem.DoesNotExist:
                return Response(f"Report: {report_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("ReportID: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


# =========================================================
@permission_classes((IsAuthenticated,))
class StocksSO(APIView):
    def get(self, arg):
        search = self.request.query_params.get('search', None)
        order_by = self.request.query_params.get('orderby', 'asc')

        if search is not None:
            if order_by == 'asc':
                try:
                    stocks = Stock.objects.filter(book__name__icontains=search).order_by('upload')
                    serializer = StockSerializer(stocks, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Stock.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif order_by == 'dec':
                try:
                    stocks = Stock.objects.filter(book__name__icontains=search).order_by('-upload')
                    serializer = StockSerializer(stocks, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Stock.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("Search: None, BADREQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class TradesSO(APIView):
    def get(self, arg):
        search = self.request.query_params.get('search', None)
        order_by = self.request.query_params.get('orderby', 'asc')

        if search is not None:
            if order_by == 'asc':
                try:
                    trades = Trade.objects.filter(book__name__icontains=search).order_by('upload')
                    serializer = StockSerializer(trades, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Trade.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            elif order_by == 'dec':
                try:
                    trades = Trade.objects.filter(book__name__icontains=search).order_by('-upload')
                    serializer = StockSerializer(trades, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Trade.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("Search: None, BADREQUEST", status=status.HTTP_400_BAD_REQUEST)
