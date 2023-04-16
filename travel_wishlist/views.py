# This view will handle requests to your home page.

# Replace Place.objects.get() with a call to Django convenience
# function get_object_or_404, below .

from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # creating a form from data in the request
        place = form.save(commit=False) # creating a model object from form 
        place.user = request.user
        if form.is_valid(): # validation againts DB constraints
            place.save()  # saves places to db
            return redirect('place_list')  # reloads home page.

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') # filter only the False and by name in order.
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

# return redirect ('place_visited ) as well.   #redirect to places visited
    return redirect('place_list')     #redirect to wishlist places


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()
    
    # Is this a GET request (show data + form), or a POST request (update Place object)?
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)
    
    else:

        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form })
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})
            



@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()




@login_required
def about(request):
    author = 'Oscar'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})