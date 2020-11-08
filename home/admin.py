from django.contrib import admin
from .models import Product, Comment, Emotion, Felling, Order, Category


# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment

class ProductAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
admin.site.register(Product, ProductAdmin)
admin.site.register(Emotion)
admin.site.register(Felling)
admin.site.register(Order)
admin.site.register(Category)