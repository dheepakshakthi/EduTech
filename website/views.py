from django.shortcuts import render

# Create your views here.

def index(request):
    """View for the login page."""
    return render(request, 'index.html')

