# This view will handle requests to your home page.

# Replace Place.objects.get() with a call to Django convenience
# function get_object_or_404, below .

from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # creating a form from data in the request
        place = form.save() # creating a model object from form 
        if form.is_valid(): # validation againts DB constraints
            place.save()  # saves places to db
            return redirect('place_list')  # reloads home page.

    places = Place.objects.filter(visited=False).order_by('name') # filter only the False and by name in order.
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

# return redirect ('place_visited ) as well.   #redirect to places visited
    return redirect('place_list')     #redirect to wishlist places


def about(request):
    author = 'Oscar'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})