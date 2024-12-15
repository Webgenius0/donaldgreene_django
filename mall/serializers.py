from rest_framework import serializers
from .models import Product, Category, ColorVariant, SizeVariant, Cart, CartItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ColorVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = '__all__'

class SizeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    color_variant = ColorVariantSerializer(many=True)
    size_variant = SizeVariantSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        color_variants_data = validated_data.pop('color_variant')
        size_variants_data = validated_data.pop('size_variant') 
        categories_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**categories_data)
        product = Product.objects.create(category=category,**validated_data) 
        for color_variant_data in color_variants_data: 
            color_variant, created = ColorVariant.objects.get_or_create(**color_variant_data) 
            product.color_variant.add(color_variant) 
        for size_variant_data in size_variants_data: 
            size_variant, created = SizeVariant.objects.get_or_create(**size_variant_data) 
            product.size_variant.add(size_variant) 
        return product


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['user']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = CartSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart']
