from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# Extend Django's built-in User model
class User(AbstractUser):
    name = models.CharField(max_length=70, blank=True)
    image = models.FileField(upload_to='profile_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sold = models.IntegerField(default=0)
    admin = models.BooleanField(default=False)

    def get_image(self):
        if self.image:
            return self.image.url
        return '/media/profile_images/default_profile.png'

    def __str__(self):
        return self.username

    def update_image(self, file):
        if self.image:
            self.image.storage.delete(self.image.name)
        self.image = file
        self.save()

# Product Model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('WEAPON', 'Weapon'),
        ('LEGO', 'Lego'),
        ('FIGURES', 'Figures'),
        ('POSTER', 'Poster'),
        ('COLLECTIBLE', 'Collectible'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=70)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.00)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    seen = models.IntegerField(default=0)
    brand = models.CharField(max_length=70, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    color = models.CharField(max_length=70, null=True, blank=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_image(self):
        """Return the sold version of the image if the product is sold."""
        if self.sold and self.image:
            return self.image.url.replace(".png", "_sold.png")
        return self.image.url if self.image else None

# Favourites Model
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# Followers Model
class Follower(models.Model):       
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"

# Cart Model to track products added by users
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_carts')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"

# Comment Model for user profiles
class Comment(models.Model):
    text = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_received")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.seller.username}"

# Message Model for private messaging between users
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField('Product', related_name='orders')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.user.username} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"