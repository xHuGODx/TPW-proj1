from django.shortcuts import render, redirect
from datetime import datetime
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

    context = {
        'products': products,
        'categories': categories,
        'search_query': query,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'index.html', context)