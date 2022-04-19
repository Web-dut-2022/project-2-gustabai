from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import *


def index(request):
    listings = Listing.objects.all()
    # print url of first listing
    print(listings[0].image)

    return render(request, "auctions/index.html", {
        "listings": listings,
        'masage': 'Active Listings'
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# function for create new listing
def create(request):
    if request.method == "POST":
        if not request.POST['title'] or not request.POST['description'] or not request.POST['price'] or not request.POST['category']:
            return render(request, 'auctions/create.html', {
                'message': 'All fields are required'
            })

        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/No_image_3x4.svg/1280px-No_image_3x4.svg.png'
        image = request.POST["image"] if request.POST["image"] else url
        seller = request.user
        is_active = request.POST["is_active"]
        categories = request.POST.getlist('category')

        new_listing = Listing(title=title, description=description, price=price, image=image, seller=seller,
                              is_active=is_active)
        new_listing.save()
        
        new_listing.category.set(categories)

        return redirect('index')

    else:
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            'categories': categories
            })

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.session.get('message'):
        message = request.session.get('message')
        del request.session['message']

        return render(request, "auctions/listing.html", {
            "listing": listing,
            'user':request.user,
            'message': message
        })
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        'user':request.user
    })

# add listing to watchlist
def watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    user.watchlist.add(listing)
    
    return redirect('listing', listing_id=listing.id)


def deletefromwatchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    user.watchlist.remove(listing)

    return redirect('listing', listing_id=listing.id)

def mywatchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request, 'auctions/index.html', {
        'listings': listings,
        'masage': 'My Watchlist'
    })


def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.is_active = False
    listing.save()
    return redirect('index')

def bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if float(request.POST['bid']) > float(listing.price):
        listing.price = request.POST['bid']
        listing.winner = request.user
        listing.save()
        return redirect('listing', listing_id=listing.id)
    else:
        request.session['message'] = 'Bid must be higher than current price'
        return redirect('listing', listing_id=listing.id)

def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
        })

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = category.listing_set.all()
    return render(request, 'auctions/index.html', {
        'listings': listings,
        'masage': 'Category: ' + category.name
        })

def coment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        if not request.POST['comment']:
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'message': 'Comment is required'
                })
        comment = request.POST['comment']
        new_comment = Coment(text=comment, listing=listing, user=request.user)
        new_comment.save()
        return redirect('listing', listing_id=listing.id)
    else:
        return render(request, 'auctions/listing.html', {
            'listing': listing
            })