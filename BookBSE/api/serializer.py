from rest_framework import serializers
from BookBSE.models import *


class FacultySerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Field
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class MyBookSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    faculty = serializers.StringRelatedField(read_only=True)
    field = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ('name', 'author', 'faculty', 'field')


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class AllStockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    book = MyBookSerializer(read_only=True)
    image = serializers.StringRelatedField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    upload = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Stock
        fields = ('id', 'book', 'image', 'price', 'upload', 'seller')


class StockSerializerStockID(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    book = MyBookSerializer(read_only=True)
    image = serializers.StringRelatedField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    upload = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    description = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Stock
        fields = ('id', 'book', 'image', 'price', 'upload', 'seller', 'description')

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
    book = MyBookSerializer(read_only=True)

    class Meta:
        model = Trade
        fields = '__all__'


class ReportProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProblem
        fields = '__all__'
