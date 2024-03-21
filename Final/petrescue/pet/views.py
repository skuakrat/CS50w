import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils.html import mark_safe

from .models import *

def home(request):
    return render(request, "pet/home.html")




def index(request):
    h1 = "All posts"
    search = ''
    province_id = request.GET.get('province')  
    type_id = request.GET.get('type')
    username = request.GET.get('username')
    follow = request.GET.get('follow')

    query = {}
    if province_id:
        query['province_id'] = province_id
        province = Province.objects.get(pk=province_id)
        search += f" in {province.name_en}"
    if type_id:
        query['type_id'] = type_id
        type = Type.objects.get(pk=type_id)
        h1 = type.type
    if username:
        user = User.objects.get(username=username)
        query['user_id'] = user.pk
        h1 = f"{user.username}'s Posts"
    posts = Post.objects.filter(**query).order_by('-id')

    if follow:
        follow_user = User.objects.get(username=follow)
        h1 = f"{follow_user.username}'s Followings"
        posts = follow_user.posts_liked.filter(**query).order_by('-id')
    
    

    paginator = Paginator(posts, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    types = Type.objects.all()
    provinces = Province.objects.all()

    return render(request, "pet/index.html", {
        "posts": page_obj,
        'types': types,
        'h1': h1,
        'search': h1 + search,
        'provinces': provinces
    })



def profile(request, username):

    if request.method == "POST":
        user = User.objects.get(username=username)
        url = request.POST["url"]
        user.url = url
        user.save()
        return HttpResponseRedirect(reverse("profile", kwargs={'username': username}))

    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).count()
    follows = user.posts_liked.all().count()
    return render(request, "pet/profile.html", {
        'user': user,
        'posts': posts,
        'follows': follows,

    })

def post(request, id):
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(id=id)
        body = request.POST["body"]

        comment, created = Comment.objects.get_or_create(user=user, post=post, body=body)

        return HttpResponseRedirect(reverse("post", kwargs={'id': id}))
    

    else:
        post = Post.objects.get(pk=id)
        comments = post.commentposts.all()
        return render(request, "pet/post.html", {
            'post': post,
            'comments': comments
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
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "pet/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "pet/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "pet/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "pet/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "pet/register.html")

@login_required    
def add_view(request):
    if request.method == "POST":
        user = request.user
        type = Type.objects.get(id=request.POST["type"])
        breed = Breed.objects.get(id=request.POST["breed"])
        province = Province.objects.get(id=request.POST["province"])
        address = request.POST["address"]
        name = request.POST["name"]
        body = request.POST["body"]
        url = request.POST["url"]


        post = Post.objects.create(user=user, type=type,breed=breed,province=province,address=address,name=name,body=body,url=url)
        post.save()

        posts = Post.objects.all().order_by('-id')
        return HttpResponseRedirect(reverse("index") + f"?username={user.username}")



    else:
        provinces = Province.objects.all()
        types = Type.objects.all()
        breeds = Breed.objects.all()
        breeddogs = Breed.objects.filter(type=Type.objects.get(type="Dogs"))
        breedcats = Breed.objects.filter(type=Type.objects.get(type="Cats"))
        breedfishs = Breed.objects.filter(type=Type.objects.get(type="Fish"))
        breedbirds = Breed.objects.filter(type=Type.objects.get(type="Birds"))
        breedrodents = Breed.objects.filter(type=Type.objects.get(type="Rodents"))
        breedos = Breed.objects.filter(type=Type.objects.get(type="Others"))

        return render(request, "pet/add.html", {
            'provinces': provinces,
            'types': types,
            'breeds': breeds,
            'breeddogs': breeddogs,
            'breedcats': breedcats,
            'breedfishs': breedfishs,
            'breedbirds': breedbirds,
            'breedrodents': breedrodents,
            'breedos': breedos,
        })
    

@login_required 
def dm(request, type):


    if type == 'inbox':
        dms = Dm.objects.filter(to=request.user).order_by('-id')
        h1 = "Inbox"

    if type == 'sent':
        dms = Dm.objects.filter(user=request.user).order_by('-id')
        h1 = "Sent"

    paginator = Paginator(dms, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "pet/dm.html", {
        'h1': h1,
        'dms': page_obj
    })

@login_required
def new_mail(request):

    if request.method == "GET":
        new_mail = Dm.objects.filter(to=request.user, read=False).count()
        return JsonResponse({"new_mail": new_mail})

    
@login_required 
def read(request, dm_id):

    dm = Dm.objects.get(pk=dm_id)
    dm_body_safe = mark_safe(dm.body.replace('\n', '<br />'))

    if dm.to == request.user:
        dm.read = True
        dm.save()
    

    return render(request, "pet/dm-id.html", {
            'h1': "Message",
            'dm': dm,
            'dm_body_safe': dm_body_safe
    })


@login_required   
def message(request, name):

    if request.method == "POST":
        user = request.user
        to = User.objects.get(username=name)
        topic = request.POST["topic"]
        body = request.POST["body"]

        dm = Dm.objects.create(user=user, to=to, topic=topic, body=body)
        dm.save()

        return HttpResponseRedirect(reverse("dm", kwargs={'type': "sent"}))
    
    else:

        return render(request, "pet/message.html", {
         'to': name,
        })

@login_required   
def activate(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = 1
    post.save()
    return redirect('post', id=post_id)

@login_required   
def deactivate(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = 0
    post.save()
    return redirect('post', id=post_id)

@login_required   
def fav(request, post_id):
    thispost = Post.objects.get(pk=post_id)
    user = request.user
    thispost.likes.add(user)
    thispost.save()

@login_required   
def unfav(request, post_id):
    thispost = Post.objects.get(pk=post_id)
    user = request.user
    thispost.likes.remove(user)
    thispost.save()

@login_required
def update_image(request):
    if request.method == "POST":
        user = User.objects.get(user=request.user)
        url = request.POST["url"]
        user.url = url
        user.save()





        



'''
def load(request):

    provinces = [
        "Bangkok", "Samut Prakan", "Nonthaburi", "Pathum Thani", "Phra Nakhon Si Ayutthaya", "Ang Thong",
        "Lop Buri", "Sing Buri", "Chai Nat", "Saraburi", "Chon Buri", "Rayong", "Chanthaburi", "Trat",
        "Chachoengsao", "Prachin Buri", "Nakhon Nayok", "Sa Kaeo", "Nakhon Ratchasima", "Buri Ram",
        "Surin", "Si Sa Ket", "Ubon Ratchathani", "Yasothon", "Chaiyaphum", "Amnat Charoen", "Bueng Kan",
        "Nong Bua Lam Phu", "Khon Kaen", "Udon Thani", "Loei", "Nong Khai", "Maha Sarakham", "Roi Et",
        "Kalasin", "Sakon Nakhon", "Nakhon Phanom", "Mukdahan", "Chiang Mai", "Lamphun", "Lampang",
        "Uttaradit", "Phrae", "Nan", "Phayao", "Chiang Rai", "Mae Hong Son", "Nakhon Sawan", "Uthai Thani",
        "Kamphaeng Phet", "Tak", "Sukhothai", "Phitsanulok", "Phichit", "Phetchabun", "Ratchaburi", 
        "Kanchanaburi", "Suphan Buri", "Nakhon Pathom", "Samut Sakhon", "Samut Songkhram", "Phetchaburi",
        "Prachuap Khiri Khan", "Chumphon", "Ranong", "Surat Thani", "Phang Nga", "Phuket", "Krabi",
        "Nakhon Si Thammarat", "Trang", "Phatthalung", "Satun", "Songkhla", "Pattani", "Yala", "Narathiwat"
    ]
    
    for province_name in provinces:
        province, created = Province.objects.get_or_create(name_en=province_name)
    
    return render(request, "pet/index.html", {
        "message": "message"
    })
'''

    