from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    description = models.TextField()

class Product(models.Model):
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    click = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dis_like = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Emotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    strong_positive = models.IntegerField(default=0)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)


class Felling(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    strong_positive = models.IntegerField(default=0)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    mail = models.EmailField()
    address = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='not yet')

    def __str__(self):
        return self.status