from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from app.models import *


# Create your views here.

def home(request):
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)


def contact(request):
    tparams = {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'contact.html', tparams)


def about(request):
    tparams = {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'about.html', tparams)

def profile(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        followers = user.followers.all()
        following = user.following.all()

        return render(request, 'profile.html', {'user': user, 'followers': followers, 'following': following})
    

def index(request):
    # Handle the search, category, and price filters
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 10000)

    products = Product.objects.all()

    # Apply search filter
    if query:
        products = products.filter(name__icontains=query)

    # Apply category filter
    if category:
        products = products.filter(category=category)

    # Apply price range filter
    products = products.filter(price__gte=min_price, price__lte=max_price)

    # Get unique categories for the filter
    categories = Product.objects.values_list('category', flat=True).distinct()

    # Initialize the context
    context = {
        'products': products,
        'categories': categories,
        'search_query': query,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
        'user': request.user,  # Always include the user object
    }

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's favorites if logged in
        user_favorites = Favourite.objects.filter(user=request.user).values_list('product_id', flat=True)
        context['favorite_products'] = list(user_favorites)  # Pass favorite product IDs to context

        # Handle adding/removing favorites
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)

            # Check if the user has already favorited the product
            favorite, created = Favourite.objects.get_or_create(user=request.user, product=product)

            if created:
                # If it was created, that means we added it to favorites
                favorite.save()
            else:
                # If it exists, that means we should remove it
                favorite.delete()
            
            # Redirect back to the index page after adding/removing favorites
            return redirect('index')
    else:
        # If the user is not authenticated, set the favorites key as an empty list
        context['favorite_products'] = []

    return render(request, 'index.html', context)


@login_required
def favourites(request):
    # Get the logged-in user
    user = request.user

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if product_id:
            # Attempt to remove the product from favourites
            Favourite.objects.filter(user=user, product_id=product_id).delete()

            # Redirect to the same page to avoid form resubmission issues
            return redirect('favourites')  # Make sure to use the correct URL name

    # Retrieve the favorite products for the user
    favorite_products_ids = Favourite.objects.filter(user=user).values_list('product_id', flat=True)
    favorite_products = Product.objects.filter(id__in=favorite_products_ids)

    # Get unique categories for the filter (optional)
    categories = Product.objects.values_list('category', flat=True).distinct()

    # Prepare the context for rendering the favourites page
    context = {
        'products': favorite_products,
        'categories': categories,
        'user': user,
    }

    return render(request, 'favourites.html', context)


@login_required
def product_details(request, product_id):
    # Get the product by ID and increase the view count
    product = Product.objects.get(id=product_id)
    product.seen += 1
    product.save()

    # Check if the product is already in the user's cart
    is_in_cart = Cart.objects.filter(user=request.user, product=product).exists()

    if request.method == "POST":
        # Handle "Add to Cart" request
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        
        # Redirect back to the product details page
        return redirect('product_details', product_id=product_id)

    context = {
        "product": product,
        "is_in_cart": is_in_cart,
    }
    return render(request, 'product_details.html', context)


@login_required
def cart(request):
    # Get all products in the user's cart
    cart_items = Cart.objects.filter(user=request.user)
    products = [item.product for item in cart_items]
    
    # Calculate the total value of the products in the cart
    total_value = sum(product.price for product in products)

    if request.method == 'POST':
        # Handle "Remove from Cart" functionality
        product_id = request.POST.get('product_id')
        Cart.objects.filter(user=request.user, product_id=product_id).delete()
        return redirect('cart')

    context = {
        'products': products,
        'total_value': total_value,
    }
    return render(request, 'cart.html', context)

@login_required
def following(request):
    # Get the logged-in user's followed users
    followed_users = Follower.objects.filter(follower=request.user).values_list('user', flat=True)
    followed_products = {}
    favourite_products = list(Favourite.objects.filter(user=request.user).values_list('product_id', flat=True))

    # Fetch products from followed users
    for user_id in followed_users:
        products = Product.objects.filter(user_id=user_id)
        if products.exists():
            followed_products[User.objects.get(id=user_id)] = products

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if product_id:
            product = Product.objects.get(id=product_id)
            # Check if the product is already in favourites
            if product.id in favourite_products:
                Favourite.objects.filter(user=request.user, product=product).delete()  # Remove from favourites
            else:
                Favourite.objects.create(user=request.user, product=product)  # Add to favourites
            return redirect('following')  # Redirect to avoid double submission

    context = {
        'followed_products': followed_products,
        'favourite_products': favourite_products,
    }
    return render(request, 'following.html', context)

@login_required
def myproducts(request):
    user = request.user
    
    # Handle product removal if a POST request is made
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id, user=user)
        product.delete()  # Remove the product from the database
        return redirect('myproducts')  # Redirect back to the myproducts page

    # Retrieve all products for the logged-in user
    products = Product.objects.filter(user=user)

    context = {
        'products': products,
        'user': user,
    }

    return render(request, 'myproducts.html', context)

@login_required
def addproduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        color = request.POST.get('color')
        image = request.FILES.get('image')  # For file upload

        product = Product(
            name=name,
            description=description,
            price=price,
            brand=brand,
            category=category,
            color=color,
            image=image,
            user=request.user  # Set the logged-in user as the product owner
        )
        product.save()
        return redirect('myproducts')  # Redirect to my products page after adding

    categories = Product.CATEGORY_CHOICES  # Get category choices for the form
    return render(request, 'addproduct.html', {'categories': categories})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.brand = request.POST.get('brand')
        product.category = request.POST.get('category')
        product.color = request.POST.get('color')

        if 'image' in request.FILES:
            product.image = request.FILES['image']  # Update the image if a new one is uploaded

        product.save()
        return redirect('myproducts')  # Redirect to "My Products" after saving

    categories = Product.CATEGORY_CHOICES  # For category choices in the form
    return render(request, 'editproduct.html', {'product': product, 'categories': categories})