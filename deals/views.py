from django.shortcuts import render
from .services import search_products

def home(request):
    """
    Renders the landing page with the main search bar.
    """
    return render(request, 'deals/home.html')

def search_results(request):
    """
    Handles search queries and displays compared deals.
    """
    query = request.GET.get('q', '')
    
    if query:
        results = search_products(query)
    else:
        results = []
        
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'deals/results.html', context)
