from django.urls import path
from . import views  

urlpatterns = [
    # Home & Auth
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),

    # Category listing (all categories)
    path("collections/", views.collection, name="collections"),  # <-- add slash here

    # Products by category
    path(
        "collections/<str:category_name>/",
        views.collectionviews,
        name="collection_view"   # ✅ clearer, matches your template
    ),

    # Product details
    path(
        "collections/<str:category_name>/<str:product_name>/",
        views.products_details,
        name="product_detail"
    ),
]