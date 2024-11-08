from django.contrib import admin
from .models import User, Product, Comment, Favorite, Cart, Message, Follower, Order

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(Follower)
admin.site.register(Order)
