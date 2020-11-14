from rest_framework import serializers
from BookBSE.models import *

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

# class PostStockSerializer(serializers.ModelSerializer):
# #
# #     seller = serializers.SerializerMethodField('getID')
# #     class Meta:
# #         model = Stock
# #         fields = ['book', 'edition', 'printno', 'price', 'seller', 'upload', 'update']
# #
# #     def getID(self, user):
# #         print("UserID: ", user.user_id)
# #         return user.user_id
# #
# #     def Save(self):
# #         stock = Stock(
# #             book= self.validated_data['book'],
# #             edition= self.validated_data['edition'],
# #             printno= self.validated_data['printno'],
# #             price= self.validated_data['price'],
# #             seller= self.validated_data['seller']
# #         )
# #         return stock

class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = '__all__'

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'



