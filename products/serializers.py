from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    reviews = SerializerMethodField(read_only=True)
    image = SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        return obj.image.build_url()

    def get_reviews(self, obj):
        product = Product.objects.get(id=obj.id)
        reviews = product.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
