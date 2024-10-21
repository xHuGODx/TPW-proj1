from django.db import models

# Custom User Model
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=70, unique=True)
    name = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    image = models.FileField(upload_to='profile_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_image(self, file):
        if self.image:
            self.image.storage.delete(self.image.name)
        self.image = file
        self.save()

# Product Model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.00)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    seen = models.IntegerField(default=0)
    brand = models.CharField(max_length=70, null=True, blank=True)
    category = models.CharField(max_length=70, null=True, blank=True)
    color = models.CharField(max_length=70, null=True, blank=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_image(self):
        """Return the sold version of the image if the product is sold."""
        if self.sold and self.image:
            #implementar funcao que cria a imagem nova.
            return self.image.url.replace(".png", "_sold.png")
        return self.image.url if self.image else None

# Comment Model for user profiles
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_received")

    def __str__(self):
        return f"Comment by {self.user.name} on {self.seller.name}"

# Follower Model to track user followers
class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.name} follows {self.followed.name}"

# Favorite Model to track user favorite products
class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.name} likes {self.product.name}"

# Cart Model to manage user's cart and total price
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product)  # Use Product directly
    total_price = models.FloatField(default=0.00)

    def __str__(self):
        return f"Cart {self.id} for {self.user.name} with total price: {self.total_price}"

    def calculate_total_price(self):
        """Calculate the total price of products in the cart."""
        self.total_price = sum(product.price for product in self.products.all())
        self.save()