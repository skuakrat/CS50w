from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import random
import markdown2

from . import util

class QsForm(forms.Form):
    q = forms.CharField()

class EditForm(forms.Form):
    title = forms.HiddenInput()
    content = forms.HiddenInput()

class AddPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

def add(request):
    if request.method == "POST":
        form = AddPageForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if any(filename.casefold() == s.casefold() for s in util.list_entries()):
                return render(request, "encyclopedia/cannotadd.html", {
                    "filename":filename 
                })

            else:    
                util.save_entry(filename,content)
                return HttpResponseRedirect('/wiki/'+filename)

        else:
            return render(request, "encyclopedia/add.html",{
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": AddPageForm(request.POST)
    })

def edit(request): 
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            filename = form.data["title"]
            content = form.data["contentmd"]   
            util.save_entry(filename,content)     
            return render(request, "encyclopedia/edit.html", {
                "title": filename,
                "content": content
            })  

def edit2(request): 
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            filename = form.data["title"]
            content = form.data["contentmd"]   
            util.save_entry(filename,content)     
            return HttpResponseRedirect('/wiki/'+filename)
        else:    
            return render(request, "encyclopedia/edit.html", {
                "title": filename,
                "content": content
            })  

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if any(title.casefold() == s.casefold() for s in util.list_entries()):
        titlemd = util.get_entry(title)
        content = markdown2.markdown(titlemd)
        return render(request, "encyclopedia/wiki/TITLE.html", {           
            "title": title,
            "content": content,
            "contentmd": titlemd,
            "entries": util.list_entries(),            
        })
    else:
        return render(request, "encyclopedia/wiki/notitle.html", {
            "title": title,
            })

def randompage(request):
        title = random.choice(util.list_entries())
        return HttpResponseRedirect('/wiki/'+title)

def search(request):
    if request.method == "POST":
        form = QsForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            matching = [s for s in util.list_entries() if q.casefold() in s.casefold()]
            title = ''.join(matching)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if any(q.casefold() == s.casefold() for s in util.list_entries()):
            title = q
            return HttpResponseRedirect('/wiki/'+title)
        if any(q.casefold() in s.casefold() for s in util.list_entries()):
            return render(request, "encyclopedia/search.html", {
                "results": matching,
            })
        if any(q.casefold() not in s.casefold() for s in util.list_entries()):
            return render(request, "encyclopedia/wiki/notitle.html", {
            "title": q,
            })