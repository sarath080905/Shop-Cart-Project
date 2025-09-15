from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Catagory, Product   # keep as Catagory since your model is spelled that way
from shop.form import CustomUserForm

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
    categories = Catagory.objects.filter(status=False)
    return render(request, "shop/collection.html", {"categories": categories})

# ============================
# PRODUCTS BY CATEGORY
# ============================
def collectionviews(request, category_name):
    """Show all products in a specific category."""
    category = Catagory.objects.filter(name__iexact=category_name, status=False).first()
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
    category = Catagory.objects.filter(name__iexact=category_name, status=False).first()
    if category:
        product = Product.objects.filter(
            category=category,
            name__iexact=product_name,
            status=False
        ).first()
        if product:
            return render(request, "shop/products/product_details.html", {
                "category": category,
                "category_name": category.name,
                "product": product
            })
        else:
            messages.error(request, "No such product found.")
            return redirect("collection_view", category_name=category_name)  # This matches urls.py
    else:
        messages.error(request, "No such Category found.")
        return redirect("collections")  # This matches urls.py
