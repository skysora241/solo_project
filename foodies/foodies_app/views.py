from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render(request, "index.html")

def reg(request):
    return render(request, "reg.html")

def signin(request):
    return render(request, "signin.html")

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': logged_user,
        'market': Market.objects.all()
    }
    return render(request, "dashboard.html", context)

def register(request):
    if request.method == "POST": ## validate the data
        errors = User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/reg')
        ## encrypting our pw
        ## store plaintext pw in variable
        user_pw = request.POST['pw']
        ## hash the password
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        ## test
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['first_name']=new_user.first_name
        return redirect('/main_lg')
    return redirect('/reg')

def login(request): ## logging a user in
    if request.method == "POST":
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]
        ## compare the passwords
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['first_name']=logged_user.first_name
                request.session['last_name']=logged_user.last_name
                return redirect('/main_lg')
    return redirect('/signin')

def logout(request):
    request.session.clear()
    return redirect('/main')

def profile(request, id):
    context = {
        'user' : User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def market_info(request, id):
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'market' : Market.objects.get(id=id),
        'items' : Item.objects.filter(market_id=id).all(),
        'user': logged_user
    }
    return render(request, 'market_info.html', context)

def item_info(request, id):
    logged_user = User.objects.get(id=request.session['user_id'])
    market_id=int(Item.objects.get(id=id).market_id)
    context = {
        'item' : Item.objects.get(id=id),
        'market' : Market.objects.get(id=market_id),
        'user': logged_user
    }
    return render(request, 'item_info.html', context)

def user_fav(request, id):
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'items': logged_user.favorites.all(),
        'user': logged_user
    }
    return render(request, "favorites.html", context)

def add_to_fav(request, id):
    logged_user = User.objects.get(id=request.session['user_id'])
    user_id=logged_user.id
    this_item = Item.objects.get(id=id)
    logged_user.favorites.add(this_item)
    print(this_item)
    return redirect(f'/user/{user_id}/favorites')

def remove_from_fav(request, id):
    logged_user = User.objects.get(id=request.session['user_id'])
    user_id=logged_user.id
    item_to_remove = Item.objects.get(id=id)
    logged_user.favorites.remove(item_to_remove)
    return redirect(f'/user/{user_id}/favorites')