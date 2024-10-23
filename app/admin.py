from django.contrib import admin
from .models import User, Product, Comment, Order, Message

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Message)

