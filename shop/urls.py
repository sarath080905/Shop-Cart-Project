from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Update login path to use your custom template
    path('login/', views.login_page, name='login'),
    
    # Remove the accounts/ include since we're using custom auth
    
    path('', views.home, name="home"),
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
        'collections/<str:category_name>/<str:product_name>/',
        views.products_details, 
        name='product_detail'
    ),
    path('category/<str:category_name>/<str:product_name>/', views.products_details, name='products_details'),

    # Cart
    path("cart/", views.view_cart, name="view_cart"),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Favorites
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/remove/<int:fav_id>/', views.remove_from_favorite, name='remove_from_favorite'),

    # Add to cart and favorites
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
]
