from django.shortcuts import render, redirect, get_object_or_404
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

    # Retrieve the favorite products for the user
    favorite_products_ids = Favourite.objects.filter(user=user).values_list('product_id', flat=True)
    favorite_products = Product.objects.filter(id__in=favorite_products_ids)

    # Get unique categories for the filter (optional)
    categories = Product.objects.values_list('category', flat=True).distinct()

    # Prepare the context for rendering the favorites page
    context = {
        'products': favorite_products,
        'categories': categories,
        'user': user,
    }

    return render(request, 'favourites.html', context)
@login_required
def profile(request):
    username = request.user.username
    print(f"Logged in username: {username}")  # Debug print
    user = get_object_or_404(User, username=username)
    print(f"User object retrieved: {user}")  # Debug print
    return render(request, 'profile.html', {'user': user})