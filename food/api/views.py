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
