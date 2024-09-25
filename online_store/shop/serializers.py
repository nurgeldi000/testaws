from rest_framework import serializers
from .models import *


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField('%d-%m-%Y %H:%M')

    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'parent_review', 'created_date']


class ProductListSerializer(serializers.ModelSerializer):
    product = ProductPhotosSerializer(read_only=True, many=True)
    category = CategorySerializer
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product', 'category', 'price', 'average_rating', 'date']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    ratings = RatingSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    product = ProductPhotosSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField()
    date = serializers.DateField(format='%d-%m-%Y')
    owner = UserProfileSimpleSerializer()

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'price', 'product', 'product_video',
                  'active', 'date', 'average_rating', 'ratings', 'reviews', 'owner']

    def get_average_rating(self, obj):
        return obj.get_average_rating()