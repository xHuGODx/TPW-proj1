from django.contrib import admin
from .models import User, Product, Comment, Favourite, Cart, Message, Follower, Order

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Favourite)
admin.site.register(Cart)
admin.site.register(Follower)
admin.site.register(Order)
