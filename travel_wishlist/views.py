from django.shortcuts import render, redirect, get_object_or_404
#from django.conf.urls import url
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden  # checks only preson logged in can make change.


@login_required
def place_list(request):
    """ If this is a POST request, the user clicked the Add button in the form. Check if the new place is valid,
    if so, save the new Place to the database, and redirect to this same pg. This creates a GET request to this 
    same Route.   
    If not a POST route, PLace is not valid , diplay a page with a list of places and for to add new Place.          
    """

    if request.method == 'POST':
    #create new place
        form = NewPlaceForm(request.POST)  # creating from data in the request creating a new place
        place = form.save(commit=False)  # creating a model object from form.
        place.user = request.user
        if form.is_valid():  # vaildation agaisnt DB constrants.
            place.save()    # saves place to db.
            return redirect('place_list')  # reloads home page.

    # If not a POST request, or the form is not valid, display the page.
    # with the form, and place list.
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to creat HTML (new_place_form)
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})  #dict data type.


@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited} )


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)  # add Place object. trys to get object if not found return 404 but keep working
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    #return redirect('places_visited')  can e used depending how you want to redirect the user via button objects actions.
    return redirect('place_list')  # redircts to wishlist places   


@login_required
def place_details(request, place_pk):
    place =get_object_or_404(Place, pk=place_pk)
    
    # does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden() 
     
    # is this a Get request (show data+ form), or a POST request (update Place object)?

   # if POST request, validate the form data and update.
    if request.method == 'POST':
       form = TripReviewForm(request.POST, request.FILES, instance=place)
       if form.is_valid():
           form.save()
           messages.info(request, 'Trip information updated!')
       else:
            messages.error(request, form.errors)  # refine later

       return redirect('place_details', place_pk=place_pk)
        # if GET request, show Place info and form.
        #
    else:
        if place.visited:  # make new review form
            review_form = TripReviewForm(instance=place)  # pre-populate with data from this Place instance.
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form} )
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place} )


@login_required
def delete_place(request, place_pk):
    place =get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()  
        return redirect('place_list')  # updating and returning to redirect to request to the home page, place_list.
    else:
        return HttpResponseForbidden()    

def about(request):
    author = 'Dan'
    about = 'A website to create a working list of places to visit and places that have been visted'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

