from rest_framework import serializers
from .models import Product, Category, ColorVariant, SizeVariant, Cart, CartItem, Order, OrderItem


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
    business_profile = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        # read_only_fields = ['business_profile']

    def get_business_profile(self, obj):
        # Return both the ID and the business name
        if obj.business_profile:
            return {
                "id": obj.business_profile.id,
                "name": obj.business_profile.business_name,
            }
        return None
    def create(self, validated_data):
        color_variants_data = validated_data.pop('color_variant')
        size_variants_data = validated_data.pop('size_variant') 
        categories_data = validated_data.pop('category')
        business_profile = validated_data.pop('business_profile')

        category, created = Category.objects.get_or_create(**categories_data)
        product = Product.objects.create(category=category,business_profile=business_profile,**validated_data) 

        for color_variant_data in color_variants_data: 
            color_variant, created = ColorVariant.objects.get_or_create(**color_variant_data) 
            product.color_variant.add(color_variant) 
        for size_variant_data in size_variants_data: 
            size_variant, created = SizeVariant.objects.get_or_create(**size_variant_data) 
            product.size_variant.add(size_variant) 
        return product

    def update(self, instance, validated_data):
        # Update the product fields
        category_data = validated_data.pop('category', None)
        color_variants_data = validated_data.pop('color_variant', None)
        size_variants_data = validated_data.pop('size_variant', None)

        # Update the category if provided
        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.category = category

        # Update the color variants if provided
        if color_variants_data:
            instance.color_variant.clear()
            for color_variant_data in color_variants_data:
                color_variant, _ = ColorVariant.objects.get_or_create(**color_variant_data)
                instance.color_variant.add(color_variant)

        # Update the size variants if provided
        if size_variants_data:
            instance.size_variant.clear()
            for size_variant_data in size_variants_data:
                size_variant, _ = SizeVariant.objects.get_or_create(**size_variant_data)
                instance.size_variant.add(size_variant)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated product
        instance.save()
        return instance
    

class CartItemSerializer(serializers.ModelSerializer):
    # product_name = serializers.ReadOnlyField(source='product.name')
    # subtotal = serializers.ReadOnlyField()
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']
        
    def get_subtotal(self, obj):
        return obj.subtotal()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True, source="items")

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_status', 'shipping_address',
            'shipping_city', 'shipping_state', 'shipping_zip_code', 'phone', 'email',
            'subtotal', 'shipping_cost', 'tax', 'total', 'items', 'order_items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'subtotal', 'total', 'created_at', 'updated_at']
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data["product"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )

        # Calculate and save totals
        order.subtotal = sum(item.subtotal() for item in order.items.all())
        order.total = order.subtotal + order.shipping_cost + order.tax
        order.save()

        return order
    def update(self,instance,validated_data):
        items_data = validated_data.pop("items", None)

        # Update the order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated order
        instance.save()

        # Update the order items if provided
        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(
                    order=instance,
                    product=item_data["product"],
                    quantity=item_data["quantity"],
                    price=item_data["price"],
                )

        # Calculate and save totals
        instance.subtotal = sum(item.subtotal() for item in instance.items.all())
        instance.total = instance.subtotal + instance.shipping_cost + instance.tax
        instance.save()

        return instance