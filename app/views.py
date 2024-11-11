from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import *
from django.db.models import Q
from django.contrib import messages
from app.forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password


def index(request):

    categories = Product.objects.values_list("category", flat=True).distinct()

    form = ProductFilterForm(request.GET or None, categories=categories)

    products = Product.objects.all()
    if form.is_valid():
        query = form.cleaned_data["search"]
        category = form.cleaned_data["category"]
        min_price = form.cleaned_data["min_price"]
        max_price = form.cleaned_data["max_price"]

        if query:
            products = products.filter(name__icontains=query)
        if category:
            products = products.filter(category=category)
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    context = {
        "products": products,
        "form": form,
        "user": request.user,
    }

    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list(
            "product_id", flat=True
        )
        context["favorite_products"] = list(user_favorites)

        if request.method == "POST":
            product_id = request.POST.get("product_id")
            product = Product.objects.get(id=product_id)
            favorite, created = Favorite.objects.get_or_create(
                user=request.user, product=product
            )
            if created:
                favorite.save()
            else:
                favorite.delete()
            return redirect("index")
    else:
        context["favorite_products"] = []

    return render(request, "index.html", context)


@login_required
def favorites(request):

    user = request.user

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id:

            Favorite.objects.filter(user=user, product_id=product_id).delete()

            return redirect("favorites")

    favorite_products_ids = Favorite.objects.filter(user=user).values_list(
        "product_id", flat=True
    )
    favorite_products = Product.objects.filter(id__in=favorite_products_ids)

    categories = Product.objects.values_list("category", flat=True).distinct()

    context = {
        "products": favorite_products,
        "categories": categories,
        "user": user,
    }

    return render(request, "favorites.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                return render(
                    request,
                    "register.html",
                    {"form": form, "error": "Username already taken"},
                )

            form.save()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)

            return redirect("index")

        else:

            return render(
                request, "register.html", {"form": form, "error": "Invalid form input"}
            )

    else:

        form = RegisterForm()
        return render(request, "register.html", {"form": form, "error": False})


@login_required
def product_details(request, product_id):

    product = Product.objects.get(id=product_id)
    product.seen += 1
    product.save()

    is_in_cart = Cart.objects.filter(user=request.user, product=product).exists()
    is_in_favorites = Favorite.objects.filter(
        user=request.user, product=product
    ).exists()

    if request.method == "POST":
        if "product_id" in request.POST:

            Cart.objects.get_or_create(user=request.user, product=product)

            return redirect("product_details", product_id=product_id)

        elif "message" in request.POST:

            message_text = request.POST.get("message")
            formatted_text = f"{request.user.username} is messaging you about {product.name}: {message_text}"

            Message.objects.create(
                sender=request.user, receiver=product.user, text=formatted_text
            )

        elif "favorite" in request.POST:
            if Favorite.objects.filter(user=request.user, product=product).exists():
                Favorite.objects.filter(user=request.user, product=product).delete()

            else:
                Favorite.objects.create(user=request.user, product=product)

    context = {
        "product": product,
        "is_in_cart": is_in_cart,
        "is_in_favorites": is_in_favorites,
    }
    return render(request, "product_details.html", context)


@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)
    products = [item.product for item in cart_items]

    total_value = sum(product.price for product in products)

    if request.method == "POST":

        product_id = request.POST.get("product_id")
        Cart.objects.filter(user=request.user, product_id=product_id).delete()
        return redirect("cart")

    context = {
        "products": products,
        "total_value": total_value,
    }
    return render(request, "cart.html", context)


@login_required
def following(request):

    followed_users = Follower.objects.filter(follower=request.user).values_list(
        "user", flat=True
    )
    followed_products = {}
    favorite_products = list(
        Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
    )

    for user_id in followed_users:
        products = Product.objects.filter(user_id=user_id)
        if products.exists():
            followed_products[User.objects.get(id=user_id)] = products

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id:
            product = Product.objects.get(id=product_id)

            if product.id in favorite_products:
                Favorite.objects.filter(user=request.user, product=product).delete()
            else:
                Favorite.objects.create(user=request.user, product=product)
            return redirect("following")

    context = {
        "followed_products": followed_products,
        "favorite_products": favorite_products,
    }
    return render(request, "following.html", context)


@login_required
def myproducts(request):
    user = request.user

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id, user=user)
        product.delete()
        return redirect("myproducts")

    products = Product.objects.filter(user=user)

    context = {
        "products": products,
        "user": user,
    }

    return render(request, "myproducts.html", context)


@login_required
def addproduct(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        brand = request.POST.get("brand")
        category = request.POST.get("category")
        color = request.POST.get("color")
        image = request.FILES.get("image")

        product = Product(
            name=name,
            description=description,
            price=price,
            brand=brand,
            category=category,
            color=color,
            image=image,
            user=request.user,
        )
        product.save()
        return redirect("myproducts")

    categories = Product.CATEGORY_CHOICES
    return render(request, "addproduct.html", {"categories": categories})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.brand = request.POST.get("brand")
        product.category = request.POST.get("category")
        product.color = request.POST.get("color")

        if "image" in request.FILES:
            product.image = request.FILES["image"]

        product.save()
        return redirect("myproducts")

    categories = Product.CATEGORY_CHOICES
    return render(
        request, "editproduct.html", {"product": product, "categories": categories}
    )


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})


@login_required
def messages_page(request, user_id=None):

    contacts = User.objects.filter(
        Q(messages_sent__receiver=request.user)
        | Q(messages_received__sender=request.user)
    ).distinct()

    selected_user = (
        get_object_or_404(User, id=user_id)
        if user_id
        else (contacts.first() if contacts.exists() else None)
    )

    chat_messages = (
        Message.objects.filter(
            Q(sender=request.user, receiver=selected_user)
            | Q(sender=selected_user, receiver=request.user)
        ).order_by("created_at")
        if selected_user
        else []
    )

    if request.method == "POST":

        message_text = request.POST.get("message")
        if selected_user and message_text:
            Message.objects.create(
                sender=request.user, receiver=selected_user, text=message_text
            )

            return redirect("messages_page", user_id=selected_user.id)

    context = {
        "contacts": contacts,
        "selected_user": selected_user,
        "chat_messages": chat_messages,
    }
    return render(request, "messages_page.html", context)


@login_required
def admin_page(request):

    product_query = request.GET.get("product_search", "")
    user_query = request.GET.get("user_search", "")
    comment_query = request.GET.get("comment_search", "")
    order_query = request.GET.get("order_search", "")

    products = (
        Product.objects.filter(name__icontains=product_query)
        if product_query
        else Product.objects.all()
    )

    users = (
        User.objects.filter(name__icontains=user_query)
        if user_query
        else User.objects.all()
    )

    comments = (
        Comment.objects.filter(user__name__icontains=comment_query)
        if comment_query
        else Comment.objects.all()
    )

    orders = (
        Order.objects.filter(user__username__icontains=order_query)
        if order_query
        else Order.objects.all()
    )

    if request.method == "POST":
        if "delete_product" in request.POST:
            product_id = request.POST.get("delete_product")
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect("admin_page")

        elif "delete_user" in request.POST:
            user_id = request.POST.get("delete_user")
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect("admin_page")

        elif "delete_comment" in request.POST:
            comment_id = request.POST.get("delete_comment")
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            return redirect("admin_page")

    return render(
        request,
        "admin_page.html",
        {
            "products": products,
            "users": users,
            "comments": comments,
            "orders": orders,
            "product_query": product_query,
            "user_query": user_query,
            "comment_query": comment_query,
            "order_query": order_query,
        },
    )


@login_required
def user_detail(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    logged_user = request.user

    products = Product.objects.filter(user=profile_user)
    comments_received = Comment.objects.filter(seller=profile_user)
    is_own_profile = logged_user == profile_user
    is_following = Follower.objects.filter(
        user=profile_user, follower=logged_user
    ).exists()

    followers = None
    if is_own_profile:
        followers = [
            follower.follower for follower in Follower.objects.filter(user=profile_user)
        ]

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "toggle_follow" and not is_own_profile:
            if is_following:

                Follower.objects.filter(
                    user=profile_user, follower=logged_user
                ).delete()
                messages.success(
                    request, f"You have unfollowed {profile_user.username}."
                )
            else:

                Follower.objects.create(user=profile_user, follower=logged_user)
                messages.success(
                    request, f"You are now following {profile_user.username}."
                )
            return redirect("user_detail", user_id=user_id)

        elif action == "comment" and not is_own_profile:
            text = request.POST.get("text")
            rating = request.POST.get("rating")
            if text and rating:
                Comment.objects.create(
                    text=text, rating=int(rating), user=logged_user, seller=profile_user
                )
                messages.success(request, "Your comment has been added.")
                return redirect("user_detail", user_id=user_id)

    return render(
        request,
        "user_detail.html",
        {
            "user": profile_user,
            "logged_user": logged_user,
            "comments_received": comments_received,
            "products": products,
            "is_own_profile": is_own_profile,
            "is_following": is_following,
            "followers": followers if is_own_profile else None,
        },
    )


@login_required
def checkout(request):
    user_cart = request.user.cart.all()
    total_value = sum(item.product.price for item in user_cart)

    if request.method == "POST":
        address = request.POST.get("address")
        payment_method = request.POST.get("payment")

        if not address or not payment_method:
            messages.error(request, "Please complete the address and payment method.")
            return redirect("checkout")

        order = Order.objects.create(user=request.user)

        for cart_item in user_cart:
            product = cart_item.product
            product.sold = True
            product.save()

            order.products.add(product)

            seller = product.user
            message_text = f"{order.user.username} just bought your {product.name}."

            Message.objects.create(
                sender=order.user, receiver=seller, text=message_text
            )

        user_cart.delete()

        messages.success(request, "Order confirmed! Thank you for your purchase.")
        return redirect("index")

    context = {
        "cart_items": user_cart,
        "total_value": total_value,
    }
    return render(request, "checkout.html", context)


@login_required
def profile_settings(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user.username)
        picture_form = UpdateUserImageForm()
        password_form = UpdatePasswordForm()
        profile_form = UpdateUserProfileForm(
            initial={
                "name": user.name,
                "email": user.email,
                "username": user.username,
                "description": user.description,
            }
        )

        return render(
            request,
            "profile_settings.html",
            {
                "user": user,
                "picture_form": picture_form,
                "password_form": password_form,
                "profile_form": profile_form,
            },
        )

    elif request.method == "POST" and "image" in request.FILES:
        user = User.objects.get(username=request.user.username)
        image_form = UpdateUserImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            file = request.FILES["image"]

            if file:
                user.update_image(file)
                return redirect("profile_settings")

        else:
            image_form = UpdateUserImageForm()
            return render(
                request,
                "profile_settings.html",
                {"user": user, "picture_form": image_form},
            )

    elif request.method == "POST" and "password_change" in request.POST:
        user = User.objects.get(username=request.user.username)
        password_form = UpdatePasswordForm(request.POST)
        image_form = UpdateUserImageForm()
        profile_form = UpdateUserProfileForm(
            initial={
                "name": user.name,
                "email": user.email,
                "username": user.username,
                "description": user.description,
            }
        )

        if password_form.is_valid():
            print(password_form.cleaned_data["old_password"])
            print(user.password)
            if check_password(
                password_form.cleaned_data["old_password"], user.password
            ):
                if (
                    password_form.cleaned_data["new_password"]
                    == password_form.cleaned_data["confirm_password"]
                ):

                    user.set_password(password_form.cleaned_data["new_password"])
                    request.user.password = password_form.cleaned_data["new_password"]
                    user.save()
                    return render(
                        request,
                        "profile_settings.html",
                        {
                            "user": user,
                            "password_form": password_form,
                            "image_form": image_form,
                            "profile_form": profile_form,
                            "success": "Password changed successfully!",
                        },
                    )

                else:
                    return render(
                        request,
                        "profile_settings.html",
                        {
                            "user": user,
                            "password_form": password_form,
                            "image_form": image_form,
                            "profile_form": profile_form,
                            "error": "Passwords do not match!",
                        },
                    )

            else:
                return render(
                    request,
                    "profile_settings.html",
                    {
                        "user": user,
                        "password_form": password_form,
                        "image_form": image_form,
                        "profile_form": profile_form,
                        "error": "Incorrect old password!",
                    },
                )

        else:
            return render(
                request,
                "profile_settings.html",
                {
                    "user": user,
                    "password_form": password_form,
                    "image_form": image_form,
                    "profile_form": profile_form,
                    "error": "Invalid form input!",
                },
            )

    elif request.method == "POST" and "profile_change" in request.POST:
        user = User.objects.get(username=request.user.username)
        profile_form = UpdateUserProfileForm(request.POST)

        if profile_form.is_valid():
            if user.username != profile_form.cleaned_data["username"]:
                user.username = profile_form.cleaned_data["username"]

            if user.email != profile_form.cleaned_data["email"]:
                user.email = profile_form.cleaned_data["email"]

            if user.name != profile_form.cleaned_data["name"]:
                user.name = profile_form.cleaned_data["name"]

            if user.description != profile_form.cleaned_data["description"]:
                user.description = profile_form.cleaned_data["description"]

            user.save()
            return redirect("profile_settings")

    elif request.method == "POST" and "delete_account" in request.POST:
        user = User.objects.get(username=request.user.username)
        user.delete()
        return redirect("index")
