import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.core import serializers
from django.core.serializers import serialize
from itertools import chain

from .models import User, Post, Follow


def page(request, posts):
    if posts == "all":
        aposts = Post.objects.all()
        plen = len(aposts)

    elif posts == "following":
        fuserfollowings, created = Follow.objects.get_or_create(fuser=request.user)
        fpostfollow = fuserfollowings.ffollowings.all()
        aposts = Post.objects.filter(puser__in=fpostfollow)
        plen = len(aposts)
    else:
        user = posts
        uprofile = User.objects.get(username=user)
        userposts = Post.objects.filter(puser=uprofile)
        aposts = userposts.order_by("-pdate").all()
        plen = len(aposts)

    try:
        paginator = Paginator(aposts, 10)
        totalpages = int(paginator.num_pages)
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.page(1)
        context = {
            'pagenum': page_number,
            'plen': totalpages
        }
    except User.DoesNotExist:
        return render(request, "network/login.html", {
                "message": "Log in required."
            })
    return JsonResponse(context, status=201)

def index(request):
    return render(request, "network/index.html")


@csrf_exempt
@login_required
def newpost(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    ppost = data.get("ppost", "")

    if ppost != "":
        post = Post(
            ppost = ppost,
            puser = request.user

        )
        post.save()
    return JsonResponse({"message": "Email sent successfully."}, status=201)


@csrf_exempt
@login_required
def like(request, post_id):
    postid = post_id
    if postid != "":
        thispost, created = Post.objects.get_or_create(id=postid)
        addliker = thispost.plikes.add(request.user)
    return JsonResponse({"likemessage": "You have liked this post!"}, status=201)


@csrf_exempt
@login_required
def unlike(request, post_id):
    postid = post_id
    if postid != "":
        thispost = Post.objects.get(id=postid)
        removeliker = thispost.plikes.remove(request.user)
    return JsonResponse({"likemessage": "You have unliked this post.."}, status=201)



# to follow a user
@csrf_exempt
@login_required
def follow(request, user):
        user = user

        followthis = Follow.objects.get(fuser=request.user)
        uthisfollow = User.objects.get(username=user)
        thisfollow = Follow.objects.get(fuser=uthisfollow)
        ufollowthis = User.objects.get(username=request.user)
        ffollowerslist = thisfollow.ffollowers.add(ufollowthis)
        ffollowingslist = followthis.ffollowings.add(uthisfollow)
        return JsonResponse({"Success": "You have followed this user."}, status=201)


# to unfollow a user
@csrf_exempt
@login_required
def unfollow(request, user):

        followthis = Follow.objects.get(fuser=request.user)
        uthisfollow = User.objects.get(username=user)
        thisfollow = Follow.objects.get(fuser=uthisfollow)
        ufollowthis = User.objects.get(username=request.user)
        ffollowerslist = thisfollow.ffollowers.remove(ufollowthis)
        ffollowingslist = followthis.ffollowings.remove(uthisfollow)
        return JsonResponse({"Sucess": "You have unfollowed this user"}, status=201)




# แสดง posts
@csrf_exempt
def posts(request, posts):

    if request.method != "POST":
        page = 1
    else:
        data = json.loads(request.body)
        page = data.get("page", "")

    if posts == "all":
        posts = Post.objects.all()

    elif posts == "following":
        userfollowings, created = Follow.objects.get_or_create(fuser=request.user)
        postfollow = userfollowings.ffollowings.all()
        posts = Post.objects.filter(puser__in=postfollow)

    else:
        user = posts
        uprofile = User.objects.get(username=user)
        userposts = Post.objects.filter(puser=uprofile)
        userposts = userposts.order_by("-pdate").all()
        posts = userposts.order_by("-pdate").all()
        userfollowers, created = Follow.objects.get_or_create(fuser=uprofile)
        userfollowings, created = Follow.objects.get_or_create(fuser=uprofile)

    aposts = posts.order_by("-pdate").all()
    pcount = len(aposts)
    paginator = Paginator(aposts, 10)
    totalpages = int(paginator.num_pages)
    page_number = page
    try:
        posts = paginator.get_page(page_number)
    except EmptyPage:
        posts = paginator.page(1)
    return JsonResponse([post.serialize() for post in posts], safe=False)


def profile(request, username):

    user = User.objects.get(username=username)
    profile = Follow.objects.get(fuser=user)
    return JsonResponse([profile.serialize()], safe=False)
    

@csrf_exempt
@login_required
def edit(request, post_id):
    try:
        posts = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("ppost") is not None:
            posts.ppost = data["ppost"]
        posts.save()
        return JsonResponse({"message": "Post update successfully."}, status=201)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return render(request, "network/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
