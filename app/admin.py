from django.contrib import admin
from .models import User, Product, Comment, Order

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Order)

