import datetime
import json
from django.core.files.base import ContentFile
import base64
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from food.models import *
from account.models import *


class Times(APIView):
    def get(self, arg):
        times = Time.objects.all()
        serializer = TimeSerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, arg):
        serializer = TimeSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this view is to get all available foods (foods menu)
@api_view(['GET', ])
def get_all_foods(request):
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# This class is only for operating on one food
@permission_classes((IsAuthenticated,))
class Foods(APIView):
    def post(self, arg):
        try:
            data = self.request.data

            new_data = {}
            filename = data['filename']
            file = ContentFile(base64.b64decode(data['image']), name=filename)
            food = Food()
            food.name = data['name']
            food.cost = data['price']
            food.image = file
            food.description = data['description']
            food.save()
            new_data['food_id'] = food.food_id

            return Response(new_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"BAD REQUEST! ERROR: '{e}'", status=status.HTTP_400_BAD_REQUEST)

    def get(self, arg):
        food_id = self.request.query_params.get('food_id', None)
        date = self.request.query_params.get('date', None)
        if food_id is not None:
            try:
                food = Food.objects.get(food_id=food_id)
                serves = Serve.objects.filter(food=food, date=datetime.datetime.strptime(date, '%Y-%m-%d'))
                serve_serializer = AdminServeSerializer(serves, many=True)
            except Food.DoesNotExist:
                return Response(f"food_id={food_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            return Response(serve_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("food_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def put(self, arg):
        food_id = self.request.query_params.get('food_id', None)
        if food_id is not None:
            try:
                food = Food.objects.get(food_id=food_id)
            except Food.DoesNotExist:
                return Response(f"food_id={food_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            serializer = FoodSerializer(food, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("food_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        food_id = self.request.query_params.get('food_id', None)
        if food_id is not None:
            try:
                food = Food.objects.get(food_id=food_id)
            except Food.DoesNotExist:
                return Response(f"food_id={food_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            food.delete()
            return Response(f"food_id: {food_id}, DELETED", status=status.HTTP_200_OK)
        else:
            return Response("food_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class AdminServesAll(APIView):
    def get(self, arg):
        seller_id = self.request.user.user_id

        date = self.request.query_params.get('date', None)
        if date is None:
            return Response("Date: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        serves = Serve.objects.filter(seller=seller_id, date=datetime.datetime.strptime(date, '%Y-%m-%d'))
        serializer = AdminServeSerializer(serves, many=True)

        data = json.loads(json.dumps(serializer.data))
        for x in data:
            for key in x['food'].keys():
                x[key] = x['food'][key]
            del x['food']

        result = []
        food_ids = []

        for x in data:
            if x['food_id'] not in food_ids:
                result.append(x)
                food_ids.append(x['food_id'])
        return Response(result, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AdminServes(APIView):
    def get(self, arg):
        seller_id = self.request.user.user_id

        try:
            serve = Serve.objects.get(seller=seller_id)
        except Serve.DoesNotExist:
            return Response(f"Serve NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

        serializer = AdminServeSerializer(serve, data=self.request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, arg):
        seller_id = self.request.user.user_id

        try:
            serve = Serve.objects.get(seller=seller_id)
        except Serve.DoesNotExist:
            return Response(f"Serve NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

        serializer = AdminServeSerializer(serve, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        seller_id = self.request.user.user_id

        try:
            serve = Serve.objects.get(seller=seller_id)
        except Serve.DoesNotExist:
            return Response("ERROR: Serve NOT FOUND!", status=status.HTTP_404_NOT_FOUND)
        serve.delete()
        return Response(f"seller_id: {seller_id}, DELETED", status=status.HTTP_200_OK)

    def post(self, arg):
        seller_id = self.request.user.user_id

        try:
            data = self.request.data
            food_id = data['food_id']
            times_list = data['list']

            for each in times_list:
                start_time = each['start_time']
                end_time = each['end_time']
                date = each['date']
                count = each['count']
                serve = Serve()
                serve.date = datetime.datetime.strptime(date, '%Y-%m-%d')

                try:
                    serve.food = Food.objects.get(food_id=food_id)
                except Food.DoesNotExist:
                    return Response(f"Food with food_id {food_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

                serve.start_serve_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
                serve.end_serve_time = datetime.datetime.strptime(end_time, '%H:%M:%S')

                try:
                    serve.seller = Account.objects.get(user_id=seller_id)
                except Account.DoesNotExist:
                    return Response(f"Seller with user_id {seller_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

                serve.max_count = count
                serve.remaining_count = count
                serve.save()

            return Response('Success!', status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(f"BAD REQUEST! ERROR: '{e}'", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class UserServesAll(APIView):
    def get(self, arg):
        date = self.request.query_params.get('date', None)
        if date is not None:
            date_encoded = datetime.datetime.strptime(date, '%Y-%m-%d')
            if date_encoded.date() < datetime.datetime.now().date():
                return Response("ERROR: the date of the serve is for the past!", status=status.HTTP_406_NOT_ACCEPTABLE)
            serves = Serve.objects.filter(date=date_encoded.date(), end_serve_time__gt=datetime.datetime.now())
        else:
            return Response("Date: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

        # serializer = UserAllServeSerializer(serves, many=True)
        # data = json.loads(json.dumps(serializer.data))
        # for x in data:
        #     for key in x['food'].keys():
        #         x[key] = x['food'][key]
        #     del x['food']

        data = []
        for serve in serves:
            dic = {'start_serve_time': serve.start_serve_time, 'end_serve_time': serve.end_serve_time}
            if dic not in data:
                data.append(dic)
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class UserServes(APIView):
    def get(self, arg):
        date = self.request.query_params.get('date', None)
        if date is not None:
            date_encoded = datetime.datetime.strptime(date, '%Y-%m-%d')
            if date_encoded.date() < datetime.datetime.now().date():
                return Response("ERROR: the date of the serve is for the past!", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("Date: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

        start_serve_time = self.request.query_params.get('start_time', None)
        end_serve_time = self.request.query_params.get('end_time', None)

        if start_serve_time is not None and end_serve_time is not None:
            serves = Serve.objects.filter(date=date_encoded.date(),
                                          start_serve_time__lte=start_serve_time,
                                          end_serve_time__gte=end_serve_time)

            serializer = UserServeSerializer(serves, many=True)
            data = json.loads(json.dumps(serializer.data))
            for x in data:
                for key in x['food'].keys():
                    x[key] = x['food'][key]
                del x['food']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Start_time / End_time: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class AdminHistoryByFood(APIView):
    def get(self, arg):
        seller = self.request.user

        date = self.request.query_params.get('date', None)
        if date is None or len(str(date)) == 0:
            serves = Serve.objects.filter(date=timezone.now(), seller=seller)
        else:
            serves = Serve.objects.filter(date=datetime.datetime.strptime(date, '%Y-%m-%d'), seller=seller)

        serializer = AdminServeSerializer(serves, many=True)
        data = json.loads(json.dumps(serializer.data))

        result = []
        for each in data:
            data = {'start_time': each['start_serve_time'],
                    'end_time': each['start_serve_time'],
                    'date': each['date'],
                    'remaining_count': each['remaining_count'],
                    'total_count': each['max_count'],
                    'food_id': each['food']['food_id'],
                    'food_name': each['food']['name'],
                    'food_image': each['food']['image'],
                    'food_cost': each['food']['cost']
                    }
            result.append(data)

        return Response(result, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AdminOrdersHistoryAll(APIView):
    def get(self, arg):
        date = self.request.query_params.get('date', None)

        if date is None or len(str(date)) == 0:
            orders = Order.objects.filter(last_update__date=timezone.now(), done=True)
        else:
            orders = Order.objects.filter(Q(last_update__date=datetime.datetime.strptime(date, '%Y-%m-%d'), done=True))

        serializer = OrderSerializer(orders, many=True)
        data = json.loads(json.dumps(serializer.data))

        for x in data:
            x['customer_username'] = Account.objects.get(user_id=x['customer']).first_name + ' ' + \
                                     Account.objects.get(user_id=x['customer']).last_name
            x['customer_student_id'] = Account.objects.get(user_id=x['customer']).student_id
            x['items'] = []

            for item in x['ordered_items'].split(" + "):
                start_index = item.split(",")[1].find(":")
                stop_index = item.split(",")[1].find("*")
                count = int(item.split(",")[1][start_index + 1:stop_index].strip())

                r_index = item.split(",")[1].find("R")
                price = int(item.split(",")[1][stop_index + 1:r_index].strip())

                item_dict = {'name': item.split(",")[0], 'count': count, 'price': price}
                x['items'].append(item_dict)
            del x['ordered_items']
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AdminOrdersAll(APIView):
    def get(self, arg):
        search = self.request.query_params.get('search', None)
        if search is None or len(str(search)) == 0:
            orders = Order.objects.filter(last_update__date=timezone.now(), done=False)
        else:
            orders = Order.objects.filter(last_update__date=timezone.now(), done=False,
                                          customer__first_name__icontains=search,
                                          customer__last_name__icontains=search)

        serializer = OrderSerializer(orders, many=True)
        data = json.loads(json.dumps(serializer.data))

        for x in data:
            x['customer_username'] = Account.objects.get(user_id=x['customer']).first_name + ' ' +\
                                     Account.objects.get(user_id=x['customer']).last_name
            x['customer_student_id'] = Account.objects.get(user_id=x['customer']).student_id
            x['items'] = []

            for item in x['ordered_items'].split(" + "):
                start_index = item.split(",")[1].find(":")
                stop_index = item.split(",")[1].find("*")
                count = int(item.split(",")[1][start_index + 1:stop_index].strip())

                r_index = item.split(",")[1].find("R")
                price = int(item.split(",")[1][stop_index + 1:r_index].strip())

                item_dict = {'name': item.split(",")[0], 'count': count, 'price': price}
                x['items'].append(item_dict)
            del x['ordered_items']
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class OrdersAll(APIView):
    def get(self, arg):
        customer_id = self.request.user.user_id

        orders = Order.objects.filter(customer=customer_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class OrderFinished(APIView):
    def post(self, arg):
        try:
            order_id = self.request.query_params.get('order_id', None)
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response(f"BAD REQUEST: order_id not sent or not found", status=status.HTTP_400_BAD_REQUEST)

        done = self.request.data['done']
        order.done = done
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class OrderProperties(APIView):
    def get(self, args):
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return Response(f"Order with order_id {order_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Order_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class AddOrder(APIView):
    def post(self, args):
        customer = self.request.user
        request_body = json.loads(self.request.body)

        if 'food_list' not in request_body:
            return Response("BAD REQUEST, food_list required!", status=status.HTTP_400_BAD_REQUEST)

        food_list = request_body['food_list']

        if len(food_list) == 0:
            return Response("BAD REQUEST, food_list is empty!", status=status.HTTP_400_BAD_REQUEST)

        serve_id_count_dict = {}
        for food in food_list:
            if 'serve_id' not in food:
                return Response("BAD REQUEST, serve_id required in food_list!", status=status.HTTP_400_BAD_REQUEST)
            if 'count' not in food:
                return Response("BAD REQUEST, count required in food_list!", status=status.HTTP_400_BAD_REQUEST)

            serve_id = food['serve_id']
            count = food['count']

            try:
                serve_to_choose = Serve.objects.get(serve_id=serve_id)

                end_serve_time = serve_to_choose.end_serve_time
                serve_date = serve_to_choose.date
                time_of_serve = datetime.datetime(year=serve_date.year, month=serve_date.month,
                                                  day=serve_date.day, hour=end_serve_time.hour,
                                                  minute=end_serve_time.minute, second=end_serve_time.second)

                if time_of_serve.timestamp() < datetime.datetime.now().timestamp():
                    return Response(f"Serve with serve_id {serve_id} is for the past, you can't reserve any food!")
            except Serve.DoesNotExist:
                return Response(f"Serve with serve_id {serve_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            if count > serve_to_choose.remaining_count:
                return Response(f"No more food! serve_id {serve_id} has only "
                                f"{serve_to_choose.remaining_count} food to serve",
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            serve_id_count_dict[serve_id] = count

        ordered_items_list = []
        total_price = 0

        for key in serve_id_count_dict.keys():
            serve_to_reduce_count = Serve.objects.get(serve_id=key)
            serve_to_reduce_count.remaining_count -= serve_id_count_dict[key]
            serve_to_reduce_count.save()
            ordered_items_list.append(f"{serve_to_reduce_count.food.name}, "
                                      f"Price: {serve_id_count_dict[key]} * {serve_to_reduce_count.food.cost}R")
            total_price += serve_id_count_dict[key] * serve_to_reduce_count.food.cost

        Order.objects.create(customer=customer,
                             total_price=total_price,
                             ordered_items=" + ".join(ordered_items_list))
        return Response("Order food completed successfully!", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class EditOrder(APIView):
    def put(self, arg):
        request_body = json.loads(self.request.body)

        if 'food_list' not in request_body:
            return Response("BAD REQUEST, food_list required!", status=status.HTTP_400_BAD_REQUEST)

        food_list = request_body['food_list']

        if len(food_list) == 0:
            return Response("BAD REQUEST, food_list is empty!", status=status.HTTP_400_BAD_REQUEST)

        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            try:
                order_to_edit = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return Response(f"order_id={order_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("order_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

        serve_id_count_dict = {}
        serve_id_before_count_dict = {}

        for food in food_list:
            if 'serve_id' not in food:
                return Response("BAD REQUEST, serve_id required in food_list!", status=status.HTTP_400_BAD_REQUEST)
            if 'count' not in food:
                return Response("BAD REQUEST, count required in food_list!", status=status.HTTP_400_BAD_REQUEST)

            serve_id = food['serve_id']
            count = food['count']

            try:
                serve_to_edit = Serve.objects.get(serve_id=serve_id)

                end_serve_time = serve_to_edit.end_serve_time
                serve_date = serve_to_edit.date
                time_of_serve = datetime.datetime(year=serve_date.year, month=serve_date.month,
                                                  day=serve_date.day, hour=end_serve_time.hour,
                                                  minute=end_serve_time.minute, second=end_serve_time.second)

                if time_of_serve.timestamp() < datetime.datetime.now().timestamp():
                    return Response(f"Serve with serve_id {serve_id} is for the past, you can't reserve any food!")
            except Serve.DoesNotExist:
                return Response(f"Serve with serve_id {serve_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            for order_item in order_to_edit.ordered_items.split(" + "):
                try:
                    serve_to_choose = Serve.objects.get(food__name=order_item.split(",")[0])

                    end_serve_time = serve_to_choose.end_serve_time
                    serve_date = serve_to_choose.date
                    time_of_serve = datetime.datetime(year=serve_date.year, month=serve_date.month,
                                                      day=serve_date.day, hour=end_serve_time.hour,
                                                      minute=end_serve_time.minute, second=end_serve_time.second)

                    if time_of_serve.timestamp() < datetime.datetime.now().timestamp():
                        return Response(f"Serve for food {order_item.split(',')[0]} "
                                        f"with serve_id {serve_id} is for the past, you can't edit your reserves!")

                except Serve.DoesNotExist:
                    return Response(f"Serve for food {order_item.split(',')[0]} NOT FOUND!",
                                    status=status.HTTP_404_NOT_FOUND)

                start_index = order_item.split(",")[1].find(":")
                stop_index = order_item.split(",")[1].find("*")
                before_count = int(order_item.split(",")[1][start_index + 1:stop_index].strip())

                # if serve_to_choose.remaining_count + before_count > serve_to_choose.max_count:
                #     return Response(f"ERROR: Out of capacity! serve_id {serve_id} has only "
                #                     f"{serve_to_choose.remaining_count} food to serve, "
                #                     f"that {before_count} of them are reserved by you",
                #                     status=status.HTTP_406_NOT_ACCEPTABLE)

                serve_id_before_count_dict[serve_to_choose.food.name] = before_count
            serve_id_count_dict[serve_id] = count

        ordered_items_list = []
        total_price = 0

        for key in serve_id_before_count_dict.keys():
            serve_to_change = Serve.objects.get(food__name=key)
            serve_to_change.remaining_count += serve_id_before_count_dict[key]
            serve_to_change.save()

        for key in serve_id_count_dict.keys():
            serve_to_change = Serve.objects.get(serve_id=key)
            serve_to_change.remaining_count -= serve_id_count_dict[key]
            serve_to_change.save()

            ordered_items_list.append(f"{serve_to_change.food.name}, "
                                      f"Price: {serve_id_count_dict[key]} * {serve_to_change.food.cost}R")
            total_price += serve_id_count_dict[key] * serve_to_change.food.cost

        order_to_edit.ordered_items = " + ".join(ordered_items_list)
        order_to_edit.total_price = total_price
        order_to_edit.save()
        return Response("Order food has edited successfully!", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class DeleteOrder(APIView):
    def delete(self, arg):
        order_id = self.request.query_params.get('order_id', None)

        if order_id is not None:
            try:
                order_to_delete = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return Response(f"order_id={order_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("order_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

        serve_id_before_count_dict = {}
        for order_item in order_to_delete.ordered_items.split(" + "):
            try:
                serve_to_choose = Serve.objects.get(food__name=order_item.split(",")[0])
            except Serve.DoesNotExist:
                return Response(f"Serve for food {order_item.split(',')[0]} NOT FOUND!",
                                status=status.HTTP_404_NOT_FOUND)

            end_serve_time = serve_to_choose.end_serve_time
            serve_date = serve_to_choose.date
            time_of_serve = datetime.datetime(year=serve_date.year, month=serve_date.month,
                                              day=serve_date.day, hour=end_serve_time.hour,
                                              minute=end_serve_time.minute, second=end_serve_time.second)

            if time_of_serve.timestamp() < datetime.datetime.now().timestamp():
                return Response(f"ERROR: Serve of food {order_item.split(',')[0]} has done in the past, "
                                f"We can't cancel your reservation!", status=status.HTTP_406_NOT_ACCEPTABLE)

            start_index = order_item.split(",")[1].find(":")
            stop_index = order_item.split(",")[1].find("*")
            before_count = int(order_item.split(",")[1][start_index + 1:stop_index].strip())

            if serve_to_choose.remaining_count + before_count > serve_to_choose.max_count:
                return Response(f"ERROR! Can't cancel the food {serve_to_choose.food.name} "
                                f"with serve_id {serve_to_choose.serve_id} because out of maximum")

            serve_id_before_count_dict[serve_to_choose.serve_id] = before_count

        for key in serve_id_before_count_dict.keys():
            serve_to_increase_count = Serve.objects.get(serve_id=key)
            serve_to_increase_count.remaining_count += serve_id_before_count_dict[key]
            serve_to_increase_count.save()

        order_to_delete.delete()
        return Response(f"order_id: {order_id}, DELETED", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class OrderHistory(APIView):
    def get(self, args):
        customer = self.request.user

        orders = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(orders, many=True)
        data = json.loads(json.dumps(serializer.data))

        for x in data:
            x['items'] = []
            for item in x['ordered_items'].split(" + "):
                start_index = item.split(",")[1].find(":")
                stop_index = item.split(",")[1].find("*")
                count = int(item.split(",")[1][start_index + 1:stop_index].strip())

                r_index = item.split(",")[1].find("R")
                price = int(item.split(",")[1][stop_index + 1:r_index].strip())

                item_dict = {'name': item.split(",")[0], 'count': count, 'price': price}

                try:
                    food_image = Food.objects.get(name=item_dict['name']).image.url
                    item_dict['image'] = food_image
                except Food.DoesNotExist:
                    item_dict['image'] = ""

                x['items'].append(item_dict)
            del x['ordered_items']

        return Response(data, status=status.HTTP_200_OK)
