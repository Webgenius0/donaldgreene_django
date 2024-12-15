from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class ColorVariant(models.Model):
    value = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Color: {self.value}'

class SizeVariant(models.Model):
    value = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Size: {self.value}'
    
# class ProductImage(models.Model):
#     product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(blank=True, null=True, upload_to='mall/product/images/')

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'Image for product: {self.product.name}'

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='mall/product_thumbnail/')

    color_variant = models.ManyToManyField(ColorVariant, related_name="products", blank=True, null=True)
    size_variant = models.ManyToManyField(SizeVariant, related_name="products", blank=True, null=True)

    # is_available = Boolean
    # payment_method = /cash on delivery/ card 
    # tags = models.ManyToManyField()
    # product_images = models.ManyToManyField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
    
    def __str__(self):
        return f'{self.user} Cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart'
    