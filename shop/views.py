import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Cart, Category, Product, Favorite   # Corrected model name
from shop.form import CustomUserForm
from django.contrib.auth.decorators import login_required
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

# ============================
# HOME PAGE
# ============================
def home(request):
    products = Product.objects.filter(status=0)
    return render(request, "shop/index.html", {"products": products})


# ============================
# LOGIN PAGE
# ============================
def login_page(request):
    """Render the login page."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "shop/login.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("login")


# ============================
# REGISTRATION PAGE
# ============================
def register(request):
    """Render the registration page."""
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
    return render(request, "shop/register.html", {"form": form})


# ============================
# CATEGORY LISTING
# ============================
def collection(request):
    """Show all active categories."""
    categories = Category.objects.filter(status=False)  # Corrected model name
    return render(request, "shop/collection.html", {"categories": categories})

# ============================
# PRODUCTS BY CATEGORY
# ============================
def collectionviews(request, category_name):
    """Show all products in a specific category."""
    category = Category.objects.filter(name__iexact=category_name, status=False).first()  # Corrected model name
    if category:
        products = Product.objects.filter(category=category, status=False)
        return render(request, "shop/products/index.html", {
            "products": products,
            "category_name": category.name
        })
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')  # This matches urls.py

def products_details(request, category_name, product_name):
    category = get_object_or_404(Category, name=category_name)
    # Get the first matching product instead of requiring a unique match
    product = Product.objects.filter(
        category=category, 
        name=product_name,
        status=False  # Only get active products
    ).first()
    
    if not product:
        messages.warning(request, "Product not found")
        return redirect('collections')
        
    context = {'product': product}
    return render(request, 'shop/products/product_details.html', context)

# ============================
# CART
# ============================
@login_required
def add_to_cart(request):
    """Add a product to the cart"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)

            product = get_object_or_404(Product, id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Product added to cart successfully!'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)


@login_required
def remove_from_cart(request, cart_id):
    """Remove a product from cart"""
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
            cart_item.delete()
            messages.success(request, "Item removed from cart")
        except Exception as e:
            messages.error(request, str(e))
    return redirect('view_cart')


@login_required
def view_cart(request):
    """View all cart items"""
    cart_items = Cart.objects.filter(user=request.user)
    grand_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
    })


# ============================
# FAVORITES (WISHLIST)
# ============================
@login_required
def add_to_favorites(request):
    """Add a product to favorites"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            product = get_object_or_404(Product, id=product_id)
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                product=product
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Product added to favorites successfully!'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)


@login_required
def remove_from_favorites(request, item_id):
    """Remove a product from favorites"""
    if request.method == 'POST':
        try:
            favorite = get_object_or_404(Favorite, id=item_id, user=request.user)
            favorite.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Product removed from favorites'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)


@login_required
def favorites(request):
    """View all favorites"""
    favorite_products = Favorite.objects.filter(user=request.user)
    return render(request, 'shop/favorites.html', {
        'favorite_products': favorite_products
    })

@login_required
def remove_from_favorite(request, fav_id):
    try:
        if request.method == 'POST':
            favorite = Favorite.objects.get(id=fav_id, user=request.user)
            favorite.delete()
            messages.success(request, "Item removed from favorites")
    except Favorite.DoesNotExist:
        messages.error(request, "Item not found in favorites")
    
    return redirect('favorites')