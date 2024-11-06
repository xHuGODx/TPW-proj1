from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import *
from django.db.models import Q
from django.contrib import messages
from app.forms import RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, 'register.html', {'form': form, 'error': 'Username already taken'})

            form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)

            return redirect('index')

        else:

            return render(request, 'register.html', {'form': form, 'error': 'Invalid form input'})

    else:

        form = RegisterForm()
        return render(request, 'register.html', {'form': form, 'error': False})


@login_required
def product_details(request, product_id):
    # Get the product by ID and increase the view count
    product = Product.objects.get(id=product_id)
    product.seen += 1
    product.save()

    # Check if the product is already in the user's cart
    is_in_cart = Cart.objects.filter(user=request.user, product=product).exists()

    if request.method == "POST":
        if "product_id" in request.POST:  # Handling "Add to Cart" form
            # Handle "Add to Cart" request
            Cart.objects.get_or_create(user=request.user, product=product)
            # Redirect back to the product details page
            return redirect('product_details', product_id=product_id)

        elif "message" in request.POST:  # Handling message form submission
            # Get the message text and format it
            message_text = request.POST.get("message")
            formatted_text = f"{request.user.username} is messaging you about {product.name}: {message_text}"

            # Create the message with the formatted text
            Message.objects.create(
                sender=request.user,
                receiver=product.user,  # Assuming the seller is the product's user
                text=formatted_text
            )

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


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user  # Passes the logged-in user to the template
    })

@login_required
def messages_page(request, user_id=None):
    # Get all unique users the logged-in user has communicated with
    contacts = User.objects.filter(
        Q(messages_sent__receiver=request.user) | Q(messages_received__sender=request.user)
    ).distinct()

    # Select user to display messages; default to the first user if none is specified
    selected_user = get_object_or_404(User, id=user_id) if user_id else (contacts.first() if contacts.exists() else None)

    # Get messages for the selected user
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=selected_user) | Q(sender=selected_user, receiver=request.user)
    ).order_by('created_at') if selected_user else []

    if request.method == "POST":
        # Handle sending a message
        message_text = request.POST.get("message")
        if selected_user and message_text:
            Message.objects.create(
                sender=request.user,
                receiver=selected_user,
                text=message_text
            )
            # Redirect to the same page to see the new message
            return redirect('messages_page', user_id=selected_user.id)

    context = {
        'contacts': contacts,
        'selected_user': selected_user,
        'messages': messages,
    }
    return render(request, 'messages_page.html', context)


@login_required
def admin_page(request):
    # Get search queries for each section
    product_query = request.GET.get('product_search', '')
    user_query = request.GET.get('user_search', '')
    comment_query = request.GET.get('comment_search', '')
    order_query = request.GET.get('order_search', '')  # Add search query for orders

    # Filter Products by name based on search query
    products = Product.objects.filter(name__icontains=product_query) if product_query else Product.objects.all()

    # Filter Users by name based on search query
    users = User.objects.filter(name__icontains=user_query) if user_query else User.objects.all()

    # Filter Comments by user name or seller name based on search query
    comments = Comment.objects.filter(user__name__icontains=comment_query) if comment_query else Comment.objects.all()

    # Filter Orders by user name or product name based on search query
    orders = Order.objects.filter(user__username__icontains=order_query) if order_query else Order.objects.all()

    # Check if delete actions were triggered
    if request.method == 'POST':
        if 'delete_product' in request.POST:
            product_id = request.POST.get('delete_product')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect('admin_page')
        
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('delete_user')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('admin_page')
        
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('delete_comment')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            return redirect('admin_page')

    return render(request, 'admin_page.html', {
        'products': products,
        'users': users,
        'comments': comments,
        'orders': orders,  # Add orders to the context
        'product_query': product_query,
        'user_query': user_query,
        'comment_query': comment_query,
        'order_query': order_query,  # Pass the order query
    })


@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    products = Product.objects.filter(user=user)
    comments_received = Comment.objects.filter(seller=user)
    is_own_profile = request.user == user
    is_following = Follower.objects.filter(user=user, follower=request.user).exists()

    # Get followers if the user is viewing their own profile
    if is_own_profile:
        followers = Follower.objects.filter(user=user)
        followers = [follower.follower for follower in followers]

    if request.method == "POST":
        action = request.POST.get("action")
        
        # Handle Follow/Unfollow
        if action == "toggle_follow" and not is_own_profile:
            if is_following:
                # Unfollow
                Follower.objects.filter(user=user, follower=request.user).delete()
                messages.success(request, f"You have unfollowed {user.username}.")
            else:
                # Follow
                Follower.objects.create(user=user, follower=request.user)
                messages.success(request, f"You are now following {user.username}.")
            return redirect('user_detail', user_id=user_id)

        # Handle New Comment Submission
        elif action == "comment" and not is_own_profile:
            text = request.POST.get("text")
            rating = request.POST.get("rating")
            if text and rating:
                Comment.objects.create(
                    text=text,
                    rating=int(rating),
                    user=request.user,
                    seller=user
                )
                messages.success(request, "Your comment has been added.")
                return redirect('user_detail', user_id=user_id)

    return render(request, 'user_detail.html', {
        'user': user,
        'comments_received': comments_received,
        'products': products,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'followers': followers if is_own_profile else None,
    })

@login_required
def checkout(request):
    user_cart = request.user.cart.all()
    total_value = sum(item.product.price for item in user_cart)

    if request.method == "POST":
        address = request.POST.get("address")
        payment_method = request.POST.get("payment")

        if not address or not payment_method:
            messages.error(request, "Please complete the address and payment method.")
            return redirect('checkout')

        # Create the order and mark products as sold
        order = Order.objects.create(user=request.user)
        
        for cart_item in user_cart:
            product = cart_item.product
            product.sold = True  # Mark the product as sold
            product.save()
            
            # Add the product to the order
            order.products.add(product)

            # Send a message to the seller
            seller = product.user  # The seller of the product
            message_text = f"{order.user.username} just bought your {product.name}."
            
            # Create the message for the seller
            Message.objects.create(
                sender=order.user,    # The buyer
                receiver=seller,      # The seller
                text=message_text
            )

        # Clear the user's cart after ordering
        user_cart.delete()

        messages.success(request, "Order confirmed! Thank you for your purchase.")
        return redirect('index')

    context = {
        'cart_items': user_cart,
        'total_value': total_value,
    }
    return render(request, 'checkout.html', context)