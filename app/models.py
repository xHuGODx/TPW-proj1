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
    cart = models.ManyToManyField('Product', related_name='carts', blank=True)
    favorites = models.ManyToManyField('Product', related_name='favorited_users', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

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
            # Implement function to create the new image
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

# Order Model to track orders between buyers and sellers
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_made')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_received')
    products = models.ManyToManyField(Product)
    total_price = models.FloatField(default=0.00)

    def __str__(self):
        return f"Order {self.id} from {self.buyer.name} to {self.seller.name}"

    def calculate_total_price(self):
        """Calculate the total price of products in the order."""
        self.total_price = sum(product.price for product in self.products.all())
        self.save()
