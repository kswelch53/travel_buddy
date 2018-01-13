from django.shortcuts import render, HttpResponse, redirect
# links model to view functions
from apps.app_one.models import User
from apps.app_one.models import Trip
# allows flash messages to html
from django.contrib import messages
from datetime import datetime, date

# Note: Registration and login validations are done in models.py
# users is the named route for app1; travel is the named route for app2


def index(request):
    print("This is index function in app_two views.py")

# this prevents users from getting to success page by typing url /success
# to get to success page they must be logged in (in session)

    if 'user_id' not in request.session:
        return redirect('users:index')
    else:
        print("Username is:", request.session['username'], request.session['user_id'])
        # print("User name is:", request.session['name'])
        user_id = request.session['user_id']
# This saves all the created trips in context and renders them on index.html
# Variable trips contains objects to be displayed by the for-loop in index.html
        context = {
            # 'trips': Trip.objects.all()
# lists all the trips planned by user who is logged in
            'trips': Trip.objects.filter(user_id=user_id),
# Lists all the trips planned by others
            'all_trips': Trip.objects.exclude(user_id=user_id)
        }

# users who are logged in are directed to the dashboard:
    return render(request, 'app_two/index.html', context)


# adds a travel plan (creates Trip object)
# redirects to index method for html display
# Note: Always redirect after creating an object
def add_plan(request):
    print("This is add_plan function in app_two views.py")
    if request.method == "POST":
        print("method=POST")
        print("Username is:", request.session['username'])
        print(request.POST['destination'], request.POST['plan'], request.POST['start_date'], request.POST['end_date'])

# saves post data in variables
        this_dest = request.POST['destination']
        this_plan = request.POST['plan']
        this_start = request.POST['start_date']

# check that start_date is in the future
        if this_start < str(date.today()):
            datestring = str(date.today())
            print("Today's date is:", datestring)
            print("Trip start date is:", this_start)
    # needs an error message on html
            print("The start date cannot be in the past")
            return redirect('travel:add_plan')
        else: # continue on
            this_end = request.POST['end_date']
# check that end_date is after start_date
            if this_end < this_start:
                print("Trip start date is", this_start)
                print("Trip end date is", this_end)
    #needs an error message on html
                print("The end date cannot be before the start date")
                return redirect('travel:add_plan')
            else: # continue on
# saves session user id in variable
                this_user_id = request.session['user_id']
# uses session user id to fetch User object
                this_user = User.objects.get(id=this_user_id)
                print("Ready to create a new trip!")

# creates Trip object with User object related name #disabled for testing
        this_trip = Trip.objects.create(user_id=this_user, destination=this_dest, plan=this_plan, start_date=this_start, end_date=this_end)

# saves Trip object in context for app2 Travel Dashboard page

        return redirect('travel:index')
        # return render(request, 'app_two/add_plan.html', context)

# back to app2 add_plan page if user is not logged in
    else:
        return render(request, 'app_two/add_plan.html')


# WORKING - routes to destination.html, which displays info about a user's trip
def destination(request, trip_id):
    print("This is destination function in app_two views.py")
    print("Trip ID:", trip_id)

# this variable needs to save not the session user, but the user who created a particular trip
    this_user_id = request.session['user_id']
    print("User ID:", this_user_id)

# this isn't the right filter; it's displaying ALL the other users
# it needs to filter users by trip
# should display all the users going on a trip except for the user who created the trip
    context = {
        'user': User.objects.get(id=this_user_id),
        'users': User.objects.exclude(id=this_user_id),
        'trip': Trip.objects.get(id=trip_id),
    }

    return render(request, 'app_two/destination.html', context)


# user can join another user's trip
def join_trip(request, trip_id):
    print("This is join_trip function in app_two views.py")
    print("Trip ID:", trip_id)

# gets the logged-in user
    this_user_id = request.session['user_id']
    this_user = User.objects.get(id=this_user_id)
    print("Traveler is:", this_user.name)

# gets the trip the user wants to join (trip_id sent from the link)
    this_trip = Trip.objects.get(id=trip_id)
    print("Join trip:", this_trip.destination, this_trip.plan)

# adds the trip to session user's travel itinerary by creating a new trip object linked to the user
# user_id=this_user is the user object of the logged-in user
    join_trip = Trip.objects.create(user_id=this_user, destination=this_trip.destination, start_date=this_trip.start_date, end_date=this_trip.end_date, plan=this_trip.plan)

    return redirect('travel:index')


def logout(request):
    print("This is logout function in app_two views.py")
    if request.method == 'POST':
        request.session.clear()#deletes everything in session
    return redirect('users:index')
