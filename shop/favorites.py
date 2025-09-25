def add_to_favorites(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'Please login to add items to your favorites!',
            'redirect': '/login/'
        }, status=401)
    
    # ...existing code for adding to favorites...
    
    return JsonResponse({
        'status': 'Product Added to Favorites Successfully!',
    }, status=200)