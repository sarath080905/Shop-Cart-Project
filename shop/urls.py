from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),

    # Home
    path('', views.home, name="home"),

    # Categories
    path("collections/", views.collection, name="collections"),  
    path("collections/<str:category_name>/", views.collectionviews, name="collection_view"),

    # Product details (keep ONE clean path only)
    path(
        'collections/<str:category_name>/<str:product_name>/',
        views.products_details, 
        name='product_detail'
    ),

    # Cart
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),

    # Favorites
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/remove/<int:fav_id>/", views.remove_from_favorite, name="remove_from_favorite"),

    # Actions
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("add-to-favorites/", views.add_to_favorites, name="add_to_favorites"),
]
