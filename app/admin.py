from django.contrib import admin
from .models import User, Product, Comment, Follower, Favorite, Cart

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Follower)
admin.site.register(Favorite)
admin.site.register(Cart)
