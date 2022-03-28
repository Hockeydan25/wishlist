from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    if request.method == 'POST':
    #create new place
        form = NewPlaceForm(request.POST)  # creating from data in the request
        place = form.save()  # creating a model object from form.
        if form.is_valid():  # vaildation agaisnt DB constrants.
            place.save()    # saves place to db.
            return redirect('place_list')  # reloads home page.

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to creat HTML 
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})  #dict data type.



def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited} )


def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)  # add Place object. trys to get object if not found return 404 but keep working
        place.visited = True
        place.save()

    #return redirect('places_visited')  can e used depending how you want to redirect the user via button objects actions.
    return redirect('place_list')  # redircts to wishlist places    


def about(request):
    author = 'Dan'
    about = 'A website to create a working list of places to visit and places that have been visted'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

