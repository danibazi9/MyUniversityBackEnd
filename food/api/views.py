import datetime
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .serializer import *


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
        serializer = FoodSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, arg):
        food_id = self.request.query_params.get('food_id', None)
        if food_id is not None:
            try:
                food = Food.objects.get(food_id=food_id)
            except Food.DoesNotExist:
                return Response(f"food_id={food_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            serializer = FoodSerializer(food, data=self.request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
        try:
            seller_id = self.request.user.user_id
        except:
            return Response("Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)
        try:
            serves = Serve.objects.filter(seller=seller_id)
        except:
            return Response("BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        serializer = AdminAllServeSerializer(serves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AdminServes(APIView):
    def get(self, arg):
        try:
            seller_id = self.request.user.user_id
        except:
            return Response(f"seller_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        try:
            serve = Serve.objects.get(seller=seller_id)
        except:
            return Response(f"food_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        serializer = AdminServeSerializer(serve, data=self.request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, arg):
        try:
            seller_id = self.request.user.user_id
        except:
            return Response("Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)
        try:
            serve = Serve.objects.get(seller=seller_id)
        except Serve.DoesNotExist:
            return Response("Serve: NOT FOUND!", status=status.HTTP_404_NOT_FOUND)
        serializer = AdminServeSerializer(serve, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        try:
            seller_id = self.request.user.user_id
        except:
            return Response("Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)
        try:
            serve = Serve.objects.get(seller=seller_id)
        except Serve.DoesNotExist:
            return Response("BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        serve.delete()
        return Response(f"seller_id: {seller_id}, DELETED", status=status.HTTP_200_OK)

    def post(self, arg):
        try:
            seller_id = self.request.user.user_id
        except:
            return Response("Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)
        try:
            serve = Serve.objects.get(seller=seller_id)
        except Serve.DoesNotExist:
            return Response("BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        serializer = AdminServeSerializer(serve, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class UserServesAll(APIView):
    def get(self, arg):
        try:
            user_id = self.request.user.user_id
        except:
            return Response("Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        serves = Serve.objects.filter(date=datetime.datetime.now())
        serializer = UserAllServeSerializer(serves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class UserServes(APIView):
    def get(self, arg):
        try:
            user_id = self.request.user.user_id
        except:
            return Response("Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        start_serve_time = self.request.query_params.get('start_time', None)
        end_serve_time = self.request.query_params.get('end_time', None)

        if start_serve_time is not None and end_serve_time is not None:
            serves = Serve.objects.filter(date=datetime.datetime.now(),
                                          start_serve_time__lte=start_serve_time,
                                          end_serve_time__gte=end_serve_time)

            serializer = UserServeSerializer(serves, data=self.request.data, many=True)
            if serializer.is_valid():
                data = json.loads(json.dumps(serializer.data))
                for x in data:
                    for key in x['food'].keys():
                        x[key] = x['food'][key]
                    del x['food']
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Start_time / End_time: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class OrdersAll(APIView):
    def get(self, arg):
        try:
            customer_id = self.request.user.user_id
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(customer=customer_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class OrderProperties(APIView):
    def get(self, args):
        try:
            user_id = self.request.user.user_id
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        order_id = self.request.query_params.get('orderID', None)
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
        try:
            customer = self.request.user
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        request_body = json.loads(self.request.body)

        if 'food_list' not in request_body:
            return Response("BAD REQUEST, food_list required!", status=status.HTTP_400_BAD_REQUEST)

        food_list = request_body['food_list']

        if len(food_list) == 0:
            return Response("BAD REQUEST, food_list is empty!", status=status.HTTP_400_BAD_REQUEST)

        serveid_count_dict = {}
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

            serveid_count_dict[serve_id] = count

        ordered_items_list = []
        total_price = 0

        for key in serveid_count_dict.keys():
            serve_to_reduce_count = Serve.objects.get(serve_id=key)
            serve_to_reduce_count.remaining_count -= serveid_count_dict[key]
            serve_to_reduce_count.save()
            ordered_items_list.append(f"{serve_to_reduce_count.food.name}, "
                                      f"Price: {serveid_count_dict[key]} * {serve_to_reduce_count.food.cost}R")
            total_price += serveid_count_dict[key] * serve_to_reduce_count.food.cost

        Order.objects.create(customer=customer,
                             total_price=total_price,
                             ordered_items=" + ".join(ordered_items_list))
        return Response("Order food completed successfully!", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class EditOrder(APIView):
    def put(self, arg):
        try:
            customer = self.request.user
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

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

        serveid_count_dict = {}
        serveid_before_count_dict = {}
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

            before_count = 0
            dict_of_found = {}
            for order_item in order_to_edit.ordered_items.split(" + "):
                dict_of_found[order_item.split(",")[0]] = False
                if order_item.split(",")[0] == serve_to_choose.food.name:
                    start_index = order_item.split(",")[1].find(":")
                    stop_index = order_item.split(",")[1].find("*")
                    before_count = int(order_item.split(",")[1][start_index + 1:stop_index].strip())
                    dict_of_found[order_item.split(",")[0]] = True
                    break

            for key in dict_of_found:
                if not dict_of_found[key]:
                    serve_to_increase_count = Serve.objects.get(food__name=key)
                    serve_to_increase_count.remaining_count += count
                    serve_to_increase_count.save()

            if count > serve_to_choose.remaining_count + before_count:
                return Response(f"No more food! serve_id {serve_id} has only "
                                f"{serve_to_choose.remaining_count + before_count} food to serve, "
                                f"that {before_count} of them are reserved by you",
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            serveid_count_dict[serve_id] = count
            serveid_before_count_dict[serve_id] = before_count

        ordered_items_list = []
        total_price = 0

        for key in serveid_count_dict.keys():
            serve_to_reduce_count = Serve.objects.get(serve_id=key)
            serve_to_reduce_count.remaining_count += serveid_before_count_dict[key]
            serve_to_reduce_count.remaining_count -= serveid_count_dict[key]
            serve_to_reduce_count.save()
            ordered_items_list.append(f"{serve_to_reduce_count.food.name}, "
                                      f"Price: {serveid_count_dict[key]} * {serve_to_reduce_count.food.cost}R")
            total_price += serveid_count_dict[key] * serve_to_reduce_count.food.cost

        order_to_edit.ordered_items = " + ".join(ordered_items_list)
        order_to_edit.total_price = total_price
        order_to_edit.save()
        return Response("Order food has edited successfully!", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class DeleteOrder(APIView):
    def delete(self, arg):
        try:
            customer = self.request.user
        except:
            return Response(f"Authentication Error! Invalid token", status=status.HTTP_400_BAD_REQUEST)

        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            try:
                order_to_delete = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return Response(f"order_id={order_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("order_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

        serveid_before_count_dict = {}
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

            serveid_before_count_dict[serve_to_choose.serve_id] = before_count

        for key in serveid_before_count_dict.keys():
            serve_to_increase_count = Serve.objects.get(serve_id=key)
            serve_to_increase_count.remaining_count += serveid_before_count_dict[key]
            serve_to_increase_count.save()

        order_to_delete.delete()
        return Response(f"order_id: {order_id}, DELETED", status=status.HTTP_200_OK)
