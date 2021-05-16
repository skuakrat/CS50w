from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

from .models import *


def close(request, item_id):
    if request.method == "POST":
        user = request.user

        if user.id is not None:
            item =  Item.objects.get(pk=int(item_id))
            status = request.POST["status"]
            
            item.status = status
            item.save()
        
            return HttpResponseRedirect(reverse("item", args=(item_id,)))
 
        else:
            return render(request, "auctions/login.html" , {
                "message": "Please log in to close your bid"
            })
    
    else:
        return render(request, "auctions/login.html" , {
                "message": "Please log in to close your bid"
        })

def item(request, item_id):
    user = request.user
    userid = request.user.id
    item = Item.objects.get(id=item_id)
    bids = Bid.objects.filter(bitem=item_id).order_by('-bdate')
    winner = bids.first()
    comments = Comment.objects.filter(citem=item_id).order_by('-cdate')
    if userid is not None:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        itemlist = watcher.witem.all()
        wlno = len(itemlist)
        if item in itemlist:
            watching = "yes"
        if item not in itemlist:
            watching = "no"
        if item.ibid == 0.00:
            bidmin = item.iprice
        if item.ibid != 0.00:
            bidmin = item.ibid+Decimal(0.01)

        return render(request, "auctions/item.html", {
            "item": item,
            "bids": bids,
            "watching": watching,
            "bidmin": bidmin,
            "winner": winner,
            "comments": comments,
            "wlno": wlno
        })
    else:
        return render(request, "auctions/item.html", {
            "item": item,
            "bids": bids,
            "winner": winner,
            "comments": comments
        })


def category(request):
    user = request.user
    if user.id is not None:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        itemlist = watcher.witem.all()
        wlno = len(itemlist)
        return render(request, "auctions/category.html",{
            "categorys": Category.objects.all(),
            "wlno": wlno
        })
    else:
        return render(request, "auctions/category.html",{
            "categorys": Category.objects.all(),
        })

def catview(request, category_id):
    user = request.user
    if user.id is not None:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        itemlist = watcher.witem.all()
        wlno = len(itemlist)
        cat = Category.objects.get(id=category_id)
        catlists = Item.objects.filter(cat=category_id, status=1).order_by('-idate')
        return render(request, "auctions/category.html",{
            "categorys": Category.objects.all(),
            "items": catlists,
            "cat": cat,
            "wlno": wlno
            })

    else:
        cat = Category.objects.get(id=category_id)
        catlists = Item.objects.filter(cat=category_id, status=1).order_by('-idate')
        return render(request, "auctions/category.html",{
            "categorys": Category.objects.all(),
            "items": catlists,
            "cat": cat,
        })

def create(request):
    user = request.user
    categorys = Category.objects.all()
    if user.id is not None:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        itemlist = watcher.witem.all()
        wlno = len(itemlist)
        if request.method == "POST":
            iuser = User.objects.get(pk=int(request.POST["iuser"]))
            item = request.POST["item"]
            cat = Category.objects.get(pk=int(request.POST["cat"]))
            price = Decimal(request.POST["iprice"])
            iprice = Decimal(price)
            ibid = Decimal(0.00)
            url = request.POST["url"]
            des = request.POST["des"]
            status = "1"
            watcher, created = Watchlist.objects.get_or_create(wuser=user)
            itemlist = watcher.witem.all()
            wlno = len(itemlist)
            createitem = Item.objects.create(iuser=iuser, item=item, cat=cat, iprice=iprice, ibid=ibid, url=url, des=des, status=status)
            createitem.save()
            return render(request, "auctions/index.html",{
                "message": "Successully added your listing.",
                "items": Item.objects.filter(status=1).order_by('-idate'),
                "wlno": wlno,
                "categorys": categorys
            })
 
        else:
            return render(request, "auctions/create.html", {
                "wlno": wlno,
                "categorys": categorys
            })
    
    else:
        return render(request, "auctions/login.html", {
            "message": "Please log in to create new listing.",
            "categorys": categorys
        })

def bid(request, item_id):
    user = request.user
    if user.id is not None:
        if request.method == "POST":
            buser = user
            bitem =  Item.objects.get(pk=int(item_id))
            bprice = Decimal(request.POST["bprice"])
            ibid = Decimal(bprice)
            
            createbid = Bid.objects.create(buser=buser, bitem=bitem, bprice=bprice)
            createbid.save()
            bitem.ibid = bprice
            bitem.save()
        
            return HttpResponseRedirect(reverse("item", args=(item_id,)))
 
        else:
            return HttpResponseRedirect(reverse("item", args=(item_id,)))
    
    else:
        return render(request, "auctions/login.html", {
            "message": "Please log in to start your bid"
        })


def comment(request, item_id):
    if request.method == "POST":
        user = request.user

        if user.id is not None:
            cuser = user
            citem =  Item.objects.get(pk=int(item_id))
            comment = request.POST["comment"]
            
            createcomment = Comment.objects.create(cuser=cuser, citem=citem, comment=comment)
            createcomment.save()
        
            return HttpResponseRedirect(reverse("item", args=(item_id,)))
 
        else:
            return render(request, "auctions/login.html", {
                "message": "Please log in to comment"
            })
    
    else:
        return render(request, "auctions/login.html", {
            "message": "Please log in to comment"
        })

def watchlist(request):
    user = request.user
    try:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
    except User.DoesNotExist:
        raise Http404("User not found.")
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlists": watcher.witem.all(),
        "wlno": len(watcher.witem.all())
    })


def index(request):
    user = request.user
    if user.id is not None:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        return render(request, "auctions/index.html", {
            "items": Item.objects.filter(status=1).order_by('-idate'),
            "wlno": len(watcher.witem.all())
        })
    else:
        return render(request, "auctions/index.html", {
            "items": Item.objects.filter(status=1).order_by('-idate'),
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


def watch(request, item_id):
    user = request.user
    try:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        item = Item.objects.get(id=item_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no item chosen")
    except Item.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: item does not exist")
    except Watchlist.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: user does not exist")
    watcher.witem.add(item)
    return HttpResponseRedirect(reverse("item", args=(item_id,)))    


def unwatch(request, item_id):
    user = request.user
    try:
        watcher, created = Watchlist.objects.get_or_create(wuser=user)
        item = Item.objects.get(id=item_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no item chosen")
    except Item.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: item does not exist")
    except Watchlist.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: user does not exist")
    watcher.witem.remove(item)
    return HttpResponseRedirect(reverse("item", args=(item_id,))) 