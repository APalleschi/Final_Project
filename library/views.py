import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Section, Comment, Listing, User


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','author', 'description', 'image_url', 'section', 'restricted']

    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


def sections(request):
    return render(request, "library/sections.html", {
        "sections": Section.objects.order_by("name").all()
    })

#need to filter this for section=restricted only
def section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    listings = Listing.objects.filter(active=True, section=section).order_by("-creation_time").all()
    return render(request, "library/index.html", {
        "title": f"Books in {section.name}",
        "listings": listings
    })


def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "library/create.html", {
                "form": form
            })
    else:
        return render(request, "library/create.html", {
            "form": CreateListingForm()
        })


def index(request):
    listings = Listing.objects.filter(active=True).order_by("-creation_time").all()
    return render(request, "library/index.html", {
        "title": "Books",
        "listings": listings
    })
    
def welcome(request):
    return render(request, "library/welcome.html")


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    on_loan = request.user.is_authenticated and (listing in request.user.loan.all())
    return render(request, "library/listing.html", {
        "comments": listing.comments.order_by("-creation_time").all(),
        "listing": listing,
        "on_loan" : on_loan
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
            return render(request, "library/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "library/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    listings = user.listings.filter(active=True).order_by("-creation_time").all()
    return render(request, "library/index.html", {
        "title": f"Books by {user.username}",
        "listings": listings
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "library/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "library/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "library/register.html")

# loans
@login_required
def loan(request):
    listings = request.user.loan.order_by("-creation_time").all()
    return render(request, "library/index.html", {
        "title": "Loaned Books",
        "listings": listings
    })

@login_required
def loan_add(request):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.loan.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def loan_delete(request):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.loan.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

#restricted section
@login_required
def restricted(request):
    # listings = request.user.loan.order_by("-creation_time").all()
    listings = Listing.objects.filter(restricted=True).order_by("-creation_time").all()
    return render(request, "library/index.html", {
        "title": "Restricted Books",
        "listings": listings
    })



